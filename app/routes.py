from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timezone
import requests
import os

#DEFINE BLUEPRINTS
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#----------- HELPER FUNCTIONS -----------
def validate_video_id(video_id):
    try: 
        video_id == int(video_id)
    except:
        abort(400, {"message": f"video {video_id} was not found"})
    return Video.query.get_or_404(video_id)

#----------- CREATE ---------------------
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response(jsonify({"details" : "Request body must include title."}), 400)
    if "release_date" not in request_body:
        return make_response(jsonify({"details" : "Request body must include release_date."}), 400)
    if "total_inventory" not in request_body:
        return make_response(jsonify({"details" : "Request body must include total_inventory."}), 400)
    
    new_video = Video(
        title=request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
    )

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()),201)

#----------- GET ---------------------
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response=[]
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    video = validate_video_id(id)
    request_body = request.get_json
    return jsonify(video.to_dict())