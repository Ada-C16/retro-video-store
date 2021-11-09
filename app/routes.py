from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from dotenv import load_dotenv
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

@videos_bp.route("", methods = ["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append(video.to_dict())

        return jsonify(videos_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response(
               {"details": "Request body must include title."}, 400
            )
        elif "release_date" not in request_body:
            return make_response(
               {"details": "Request body must include release_date."}, 400
            )
        elif "total_inventory" not in request_body:
            return make_response(
               {"details": "Request body must include total_inventory."}, 400
            )
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        return make_response(
            new_video.to_dict(), 201
        )
            


@videos_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def handle_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return {"Error": "Id must be numeric"}, 400
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    if request.method == "GET":
        return video.to_dict()
        
    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(
               {"message": "Invalid data"}, 400
            )
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response(video.to_dict(), 200)

