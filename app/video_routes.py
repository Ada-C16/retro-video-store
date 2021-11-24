from flask import Blueprint, abort, jsonify, make_response, request

from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from app.rental_routes import deletes_rentals

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('', methods=['GET', 'POST'])
def handle_videos():
    if request.method == 'GET':
        videos = Video.query.all()
        return jsonify([video.to_dict() for video in videos]), 200

    elif request.method == 'POST':
        request_body = request.get_json()
        return post_single_or_multiple_video(request_body)

@videos_bp.route('/<id_num>', methods=['GET', 'PUT', 'DELETE'])
def handle_video(id_num):
    validate_video_id(id_num)
    
    video = Video.query.get(id_num)
    
    if request.method == 'GET':
        return jsonify(video.to_dict()), 200

    elif request.method == 'PUT':
        request_body = request.get_json()
        validate_video(request_body)
        
        for key, value in request_body.items():
            if key in Video.__table__.columns.keys():
                setattr(video, key, value)

        db.session.commit()
        return jsonify(video.to_dict()), 200
    
    elif request.method == 'DELETE':
        deletes_rentals(video.video_id)
        db.session.delete(video)
        db.session.commit()
        return jsonify({"id": video.video_id}), 200

@videos_bp.route('/<id_num>/rentals', methods=['GET'])
def handle_video_rentals(id_num):
    validate_video_id(id_num)

    all_rentals = []
    rentals = db.session.query(Rental).filter(Rental.video_id == id_num).all()
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        all_rentals.append({"name": customer.name})

    return make_response(jsonify(all_rentals), 200)

# HELPER FUNCTIONS
def validate_video(request_body):
    valid_keys = ['title', 'release_date', 'total_inventory']
    if not request_body:
        abort(make_response(jsonify({"error": "No data was sent"}), 400))

    for key in valid_keys:
        if key not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {key}."}), 400))

def create_video(data):
    new_video = Video(
        title = data['title'],
        release_date = data['release_date'],
        total_inventory = data['total_inventory']
    )
    return new_video

def post_single_or_multiple_video(request_body):
    #checks for list if we want to post multiple videos
    if isinstance(request_body, list):
        for video in request_body:
            validate_video(video)
                
            new_video = create_video(video)
            db.session.add(new_video)
            return jsonify({"video": video.to_dict()} for video in request_body), 201
        
    else:
        validate_video(request_body)
            
        new_video = create_video(request_body)
        db.session.add(new_video)
        db.session.commit()
        return jsonify(new_video.to_dict()), 201

def validate_video_id(id_num):
    try:
        id_num = int(id_num)
    except ValueError:
        abort(make_response(jsonify({"error": "Invalid ID"}), 400))

    video = Video.query.get(id_num)
    if not video:
        abort(make_response(jsonify({"message": f"Video {id_num} was not found"}), 404))
