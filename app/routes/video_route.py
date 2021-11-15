
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.video import Video
from app.models.rental import Rental
from .helpers import id_is_valid, request_has_all_required_categories, sort_limit_and_paginate

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def handle_videos():
    videos = sort_limit_and_paginate(Video())
    videos_response = [video.to_json() for video in videos]
    return jsonify(videos_response), 200

@videos_bp.route("", methods=["POST"])
def add_video():
    request_body, error_msg = request_has_all_required_categories("video")
    if error_msg is not None:
        return error_msg
        
    video = Video().new_video(request_body)
    db.session.add(video)
    db.session.commit()

    return jsonify(video.to_json()), 201

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
        
    rentals = Rental.query.filter_by(video_id=int(video_id))

    customer_details_response = []
    for rental in rentals:
        customer_details_response.append(rental.customer_details())

    return jsonify(customer_details_response), 200

