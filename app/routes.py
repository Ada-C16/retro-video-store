from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, request, jsonify
from datetime import datetime
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return jsonify(response_body)

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    if "release_date" not in request_body:
        return {"details": "Request body must include release_date."}, 400
    if "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400

    new_video = Video(
        title= request_body["title"],
        release_date= request_body["release_date"],
        total_inventory= request_body["total_inventory"]
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

@videos_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        video = Video.query.get(video_id)
    except:
        return jsonify(None), 400

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    return video.to_dict()

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    db.session.delete(video)
    db.session.commit()

    return video.to_dict()

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    request_body = request.get_json()
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    if "release_date" not in request_body:
        return {"details": "Request body must include release_date."}, 400
    if "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400


    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    db.session.commit()

    return video.to_dict()