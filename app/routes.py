from flask import Blueprint, jsonify, make_response, request
from app.models.video import Video
from app import db

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)
