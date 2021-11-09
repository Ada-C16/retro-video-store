from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('', methods=['GET', 'POST'])
def handle_videos():
    if request.method == 'GET':
        videos = Video.query.all()
        return jsonify([video.to_dict() for video in videos]), 200

    elif request.method == 'POST':
        request_body = request.get_json()
        
        #checks for list if we want to post multiple videos
        if isinstance(request_body, list):
            for video in request_body:
                if validate_video(video) != True:
                    return validate_video(video)
                
                new_video = Video(
                    title = video['title'],
                    release_date = video['release_date'],
                    total_inventory = video['total_inventory']
                )
                db.session.add(new_video)
                return jsonify({"video": video.to_dict()} for video in request_body), 201
        
        else:
            if validate_video(request_body) != True:
                return validate_video(request_body)
            
            new_video = Video(
                title = request_body['title'],
                release_date = request_body['release_date'],
                total_inventory = request_body['total_inventory']
            )
            db.session.add(new_video)
            db.session.commit()
            return jsonify(new_video.to_dict()), 201

@videos_bp.route('/<id_num>', methods=['GET', 'PUT', 'DELETE'])
def handle_video(id_num):
    try:
        id_num = int(id_num)
    except ValueError:
        return make_response(jsonify({"error": "Invalid ID"}), 400)

    video = Video.query.get(id_num)
    if not video:
        return make_response(jsonify({"message": f"Video {id_num} was not found"}), 404)
    
    if request.method == 'GET':
        return jsonify(video.to_dict()), 200

    elif request.method == 'PUT':
        request_body = request.get_json()
        if validate_video(request_body) != True:
            return validate_video(request_body)
        
        for key, value in request_body.items():
            if key in Video.__table__.columns.keys():
                setattr(video, key, value)
                
        db.session.commit()
        return jsonify(video.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(video)
        db.session.commit()
        return jsonify({"id": video.id}), 200


def validate_video(response_body):
    if not response_body:
        return make_response(jsonify({"error": "No data was sent"}), 400)
    elif 'title' not in response_body:
        return make_response(jsonify({"details": "Request body must include title."}), 400)
    elif 'release_date' not in response_body:
        return make_response(jsonify({"details": "Request body must include release_date."}), 400)
    elif 'total_inventory' not in response_body:
        return make_response(jsonify({"details": "Request body must include total_inventory."}), 400)
    else:
        return True