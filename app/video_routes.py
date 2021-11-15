from datetime import datetime

from flask import Blueprint, jsonify, request

from app import db
from app.models.customer import Customer
from app.models.video import Video

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()

    videos_response = [video.create_dict() for video in videos]

    if not videos_response:
        videos = Video.query.all()
        videos_response = [video.create_dict() for video in videos]

    return jsonify(videos_response)


@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    if "title" not in request_body:
        response_body = {"details": "Request body must include title."}
        return jsonify(response_body), 400
    elif "release_date" not in request_body:
        response_body = {"details": "Request body must include release_date."}
        return jsonify(response_body), 400
    elif "total_inventory" not in request_body:
        response_body = {"details": "Request body must include total_inventory."}
        return jsonify(response_body), 400
    new_video = Video.from_json()
    video_response = new_video.create_dict()
    return jsonify(video_response), 201


@videos_bp.route("/<video_id>", methods=["GET"])
def get_videos_by_id(video_id):
    if not video_id.isnumeric():
        return jsonify(None), 400
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": "Video 1 was not found"}), 404

    response_body = video.create_dict()
    return jsonify(response_body), 200


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    video.deleted_at = datetime.now()
    delete_message = video.create_dict()
    db.session.delete(video)
    db.session.commit()

    return jsonify(delete_message), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def put_video_by_id(video_id):
    form_data = request.get_json()
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        error_dict = {"details": "Invalid data"}
        return jsonify(error_dict), 400
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    video.update(form_data)

    response_body = video.create_dict()
    return jsonify(response_body), 200


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_id(video_id):

    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    customer_ids = [rental.id for rental in video.rentals]
    if not customer_ids:
        return jsonify([]), 200

    response_body = [Customer.query.get(
        customer).customer_dict() for customer in customer_ids]
    return jsonify(response_body), 200
