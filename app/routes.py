from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models.video import Video
from app import db
from sqlalchemy import exc
from sqlalchemy.exc import DataError
videos_bp = Blueprint("videos", __name__, url_prefix ="/videos")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@videos_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    try: 
        video = Video.query.get(video_id)
        if video:
            return jsonify(video.to_dict()), 200
        else:
            return make_response({"message": "Video 1 was not found"}), 404
    except DataError:
        return make_response({"message": "invalid video id, please enter number"}), 400


@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    elif "release_date" not in request_body: 
        return {"details": "Request body must include release_date."}, 400
    elif "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]
                    )
    db.session.add(new_video)
    db.session.commit()
    
    return make_response(new_video.to_dict()), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def change_data(video_id):
    video = Video.query.get(video_id)
    form_data = request.get_json()
    
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        return make_response({"message": "missing data"}), 400
    else:
        if video:
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]
            db.session.commit()
            return make_response({
                "title":video.title, "release_date":video.release_date, "total_inventory":video.total_inventory})
        else:
            return make_response({"message": "Video 1 was not found"}), 404

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video:
        db.session.delete(video)
        db.session.commit()
        return make_response({f"id": int(video_id)})
    else:
        return make_response({"message": "Video 1 was not found"}), 404

