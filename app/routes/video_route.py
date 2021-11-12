
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.video import Video
from app.models.rental import Rental
from .helpers import id_is_valid, request_has_all_required_categories

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["POST","GET"])
def handle_videos():
    if request.method=="POST":
        request_body, error_msg = request_has_all_required_categories("video")
        if error_msg is not None:
            return error_msg
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
            )
        db.session.add(new_video)
        db.session.commit()
        return jsonify(new_video.to_json()), 201

    elif request.method=="GET":
        videos = Video.query.all()
        videos_response = [video.to_json() for video in videos]
        return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_a_video(video_id):
    
    video, error_msg = id_is_valid(video_id, "video")
    if error_msg is not None:
        return error_msg 

    elif request.method == "GET":
        return jsonify(video.to_json()),200
                        
    elif request.method == "PUT":
        request_body, error_msg = request_has_all_required_categories("video")
        if error_msg is not None:
            return error_msg
        else:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
            db.session.commit()

            return make_response(video.to_json())

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({"id": video.id}, 200)

@videos_bp.route("<video_id>/rentals", methods=["GET"])
def video_rentals(video_id):
    _, error_msg = id_is_valid(video_id, "video")
    if error_msg is not None:
        return error_msg  
        
    all_rentals = Rental.query.all()

    rentals = []
    for rental in all_rentals:
        if rental.video_id == int(video_id):
            rentals.append(rental)
    # [rental object, rental object, rental, object]

    customer_details_response = []
    for rental_object in rentals:
        customer_details_response.append(rental_object.customer_details())

    return jsonify(customer_details_response), 200

