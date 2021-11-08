

import requests
from flask import Blueprint, request, make_response, jsonify

from app.models.video import Video


videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@videos_bp.route("", methods=["GET"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.id,
                "title": video.title,
                "total_inventory": video.total_inventory,
                "release_date": video.release_date
            })
    return jsonify(videos_response)
