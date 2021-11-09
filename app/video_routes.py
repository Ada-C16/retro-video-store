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
    # if not video_id.is_integer():
    #     return jsonify(), 400

    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": "Video 1 was not found"}), 404
    response_body = video.to_dict()
    return jsonify(response_body)