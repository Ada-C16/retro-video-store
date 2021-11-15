from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime
from flask import Blueprint, jsonify, request


videos_bp = Blueprint("videos", __name__, url_prefix=("/videos"))


@videos_bp.route("", methods=["GET"])
def get_all_videos():
    if request.method == "GET":
        video = Video.query.all()
        video_response = [video.video_information() for video in video]
    return jsonify(video_response), 200


@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify(details="Request body must include title."), 400

    if "release_date" not in request_body:
        return jsonify(details="Request body must include release_date."), 400

    if "total_inventory" not in request_body:
        return jsonify(details="Request body must include total_inventory."), 400

    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"],
    )

    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.video_information()), 201


@videos_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    return jsonify(video.video_information()), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def edit_video_data(video_id):
    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    form_data = request.get_json()

    if (
        "title" not in form_data
        or "release_date" not in form_data
        or "total_inventory" not in form_data
    ):
        return jsonify(None), 400

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]

    db.session.commit()

    return jsonify(video.video_information()), 200


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    db.session.delete(video)
    db.session.commit()

    return jsonify(id=video.id), 200


@videos_bp.route("/hello", methods=["GET"])
def get_hello():
    return jsonify(None), 400
