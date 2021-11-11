from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime
import requests
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix=("/customers"))
videos_bp = Blueprint("videos_bp", __name__, url_prefix=("/videos"))


@videos_bp.route("", methods=["GET", "POST"])

def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "description": task.description,
                "is_complete": False if task.completed_at == None else True
            })




@videos_bp.route("/<video_id>", methods= ["GET", "PUT", "DELETE"])