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


@videos_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        video = Video.query.get(video_id)
    except:
        return jsonify(None), 400

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    return video.to_dict()
