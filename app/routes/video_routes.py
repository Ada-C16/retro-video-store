from app import db
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, request, jsonify

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return jsonify(response_body)

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    error_message = validate_request(request_body)
    if error_message:
        return error_message

    new_video = Video(
        title= request_body["title"],
        release_date= request_body["release_date"],
        total_inventory= request_body["total_inventory"]
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201


@videos_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        video = Video.query.get(video_id)
    except:
        return jsonify(None), 400

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    return video.to_dict()


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    db.session.delete(video)
    db.session.commit()

    return video.to_dict()

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    request_body = request.get_json()
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    error_message = validate_request(request_body)
    if error_message:
        return error_message

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    db.session.commit()

    return video.to_dict()

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    customers = []
    for customer in video.customers:
        rental = Rental.query.filter_by(customer_id = customer.id, video_id = video_id).first()
        customer = customer.to_dict()
        customer["due_date"] = rental.due_date
        customers.append(customer)

    return jsonify(customers)

def validate_request(request_body):
    attributes = ["title", "release_date", "total_inventory"]

    for attribute in attributes:
        if attribute not in request_body:
            return {"details": f"Request body must include {attribute}."}, 400