from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from dotenv import load_dotenv
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

@videos_bp.route("", methods = ["GET"])
def handle_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append({
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        })

    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods = ["GET"])
def handle_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    return {
        "id": video.id,
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory
    }