from app.models.video import Video
from app import db
from flask import Blueprint, request, jsonify
from datetime import datetime
import os, requests, json

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@video_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    if videos is None:
        return jsonify([])
    response_body = []
    for video in videos:
        response_body.append(video.to_dict())
    return jsonify(response_body)

@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    ## try
    # if not isinstance(video_id, int):
    ## or
    # if not url_path.is_integer():
        # return jsonify(), 400

    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": "Video 1 was not found"}), 404
    response_body = video.to_dict()
    return jsonify(response_body)

@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        response_body = {}
        if "title" not in request_body:
            response_body["details"] = "Request body must include title."
        elif "release_date" not in request_body:
            response_body["details"] = "Request body must include release_date."
        elif "total_inventory" not in request_body:
            response_body["details"] = "Request body must include total_inventory"
        return jsonify(response_body), 400
    
    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
        )
    db.session.add(new_video)
    db.session.commit()

    response_body={}
    response_body["id"] = new_video.video_id
    return jsonify(response_body), 201