from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime

# setup blueprints here
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

# Customers routes

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    # response = []
    customers = Customer.query.all()
    # for customer in customers:
    #     response.append(customer.to_dict())

    response = [customer.to_dict() for customer in customers]

    return jsonify(response)

#WV1: Get No Saved Videos Get Videos One Saved Video
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    videos = Video.query.all()
    response = [video.to_dict() for video in videos]
    return jsonify(response), 200

#WV1: Create Video, Must Contain Title/Release Date/Inventory
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_all_videos():
    request_body = request.get_json()
    try:
        new_video = Video(title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"])
    except KeyError:
        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        if "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        if "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201

#WV1: Invalid Video ID, Get Video Not Found, Get Video
@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    try:
        video_id = int(video_id)
        video = Video.query.get(video_id)
    except ValueError:
        return {}, 400
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    else:
        return jsonify(video.to_dict()), 200

#WV1: Update Video, Update Video Not Found, Invalid Data
@videos_bp.route("/<video_id>", methods=["PUT"])
def update_one_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    input_data = request.get_json()
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    try:
        video.title = input_data["title"]
        video.release_date = input_data["release_date"]
        video.total_inventory = input_data["total_inventory"]
    except KeyError:
        if "title" not in input_data:
            return {}, 400
        if "release_date" not in input_data:
            return {}, 400
        if "total_inventory" not in input_data:
            return {}, 400
    db.session.commit()
    return jsonify(video.to_dict()), 200

#WV1: Delete Video, Delete Video Not Found
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    else:
        db.session.delete(video)
        db.session.commit()
        return {"id": video_id}, 200