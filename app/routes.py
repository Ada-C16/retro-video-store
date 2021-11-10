from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import date
import requests, os
from dotenv import load_dotenv

video_bp = Blueprint('video', __name__, url_prefix="/videos")
customer_bp = Blueprint('customer', __name__, url_prefix="/customers")
load_dotenv()

# Get all Videos
@video_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200

# Post a Video
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"Error": "Missing required fields for video. Must contain title, release date, and total inventory."}), 400
    
    new_video = Video(
        video_title=request_body["video_title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()
    return jsonify({"video": new_video.to_dict()}), 201

# Get one Video
@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"Error": f"Video {video_id} not found."}), 404
    return jsonify({"video": video.to_dict()}), 200

# Update a Video
@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"Error": f"Video {video_id} not found."}), 404

    request_body = request.get_json()

    video.video_title = request_body["video_title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()
    return jsonify({"video": video.to_dict()}), 200

# Delete a Video
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"Error": f"Video {video_id} not found."}), 404

    db.session.delete(video)
    db.session.commit()
    return jsonify({"message": f"Video {video_id} deleted."}), 200