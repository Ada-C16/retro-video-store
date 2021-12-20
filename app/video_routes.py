from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from dotenv import load_dotenv
load_dotenv()

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_video():
    videos = Video.query.all()

    response = []
    for video in videos:
        response.append(video.to_dict())

    return jsonify(response), 200

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    try:
        new_video = Video.from_dict(request_body)
        db.session.add(new_video)
        db.session.commit()

        return jsonify(new_video.to_dict()), 201

    except:
        if "title" not in request_body.keys():
            response = {
                "details" : "Request body must include title."
            }
        elif "release_date" not in request_body.keys():
            response = {
                "details" : "Request body must include release_date."
            }
        elif "total_inventory" not in request_body.keys():
            response = {
                "details" : "Request body must include total_inventory."
            }
        
        return jsonify(response), 400

@videos_bp.route("/<video_id>", methods=["GET"])
def get_a_video(video_id):
    if not video_id.isnumeric():
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404

    return jsonify(video.to_dict()), 200    


    
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_a_video(video_id):
    video = Video.query.get(video_id)
    
    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404
    
    else:
        db.session.delete(video)
        db.session.commit()
        return jsonify(
        {
        "id": video.video_id, #this worked but video_id didnt??
        'details': (f'Video {video.video_id} successfully deleted')
        }

        ), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def patch_a_video(video_id):
    try:

        request_body = request.get_json()

        video = Video.query.get(video_id)

        if not video:
            return jsonify({"message" : f"Video {video_id} was not found"}), 404
        else:

            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]

            db.session.commit()

            return jsonify(video.to_dict()), 200
    except KeyError:
        return jsonify(None), 400

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):
    rentals = Rental.query.filter_by(video_id=video_id)
    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message" : f"Video {video_id} was not found"}), 404

    customer_list = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        customer_list.append(customer.to_dict())

    return jsonify(customer_list), 200