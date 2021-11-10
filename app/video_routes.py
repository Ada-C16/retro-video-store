from flask.wrappers import Response
from app import db
from app.models.video import Video
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort
import requests
import inspect

# Create Blueprint

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# Helper functions

def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_video_from_id(video_id):
    valid_int(video_id, "video_id")
    video = Video.query.get(video_id)
    if video:
        return video

    abort(make_response({"message": f"Video {video_id} was not found"}, 404))

# Video CRUD routes

@videos_bp.route("", methods=["GET"])
def read_all_videos():
    videos = Video.query.all()

    response_body = [video.to_dict() for video in videos]

    return jsonify(response_body)

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        response_body = {
            "details": "Request body must include title."
        }
        return jsonify(response_body), 400
    if "release_date" not in request_body:
        response_body = {
            "details": "Request body must include release_date."
        }
        return jsonify(response_body), 400
    if "total_inventory" not in request_body:
        response_body = {
            "details": "Request body must include total_inventory."
        }
        return jsonify(response_body), 400

    new_video = Video.from_json(request_body)

    db.session.add(new_video)
    db.session.commit()

    response_body = new_video.to_dict()

    return jsonify(response_body), 201

@videos_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = get_video_from_id(video_id)

    response_body = video.to_dict()

    return jsonify(response_body)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_one_video(video_id):
    video = get_video_from_id(video_id)
    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        response_body = {
            "details": "missing required data"
        }
        return jsonify(response_body), 400

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()

    response_body = video.to_dict()

    return jsonify(response_body)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = get_video_from_id(video_id)

    db.session.delete(video)
    db.session.commit()

    response_body = {
        "id": video.id
    }

    return jsonify(response_body)