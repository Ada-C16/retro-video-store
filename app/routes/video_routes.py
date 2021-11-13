from flask import Blueprint, jsonify, make_response, request, abort
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app import db
from datetime import datetime, timezone, timedelta
import requests
import os

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def is_input_valid(number):
    try:
        int(number)
    except:
        abort(400)


def is_parameter_found(model, parameter_id):
    is_input_valid(parameter_id)
    if model.query.get(parameter_id) is None:
        return abort(make_response({"message":f"Video {parameter_id} was not found"}, 404))
    return model.query.get(parameter_id)



@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if "title" not in request_body: 
        return jsonify({"details": "Request body must include title."}), 400
    elif "release_date" not in request_body: 
        return jsonify({"details": "Request body must include release_date."}), 400
    elif "total_inventory" not in request_body:
        return jsonify({"details": "Request body must include total_inventory."}), 400

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]
                    )

    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201


@videos_bp.route("", methods=["GET"])
def read_videos():
    videos = Video.query.all()
    response_body = []
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        videos = Video.query.order_by(Video.title.asc())
    elif sort_query == "desc":
        videos  = Video.query.order_by(Video.title.desc())
    else:
        videos = Video.query.all()

    for video in videos:
        response_body.append(
            video.to_dict())
    return jsonify(response_body), 200


@videos_bp.route("/<video_id>", methods=["GET"])
def read_video(video_id):
    video = is_parameter_found(Video, video_id)
    video_response = video.to_dict()
    return jsonify(video_response), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = is_parameter_found(Video, video_id)
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()

    response_body = video.to_dict()
    return jsonify(response_body), 200


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = is_parameter_found(Video, video_id)
    rental_entries = db.session.query(Rental).filter_by(video_id=video.id).all()
    response_str = {"id": video.id}

    if rental_entries:
        for rental in rental_entries:
            db.session.delete(rental)
    db.session.delete(video)


    db.session.commit()
    return jsonify(response_str), 200

# List the customers who currently have the video checked out
@videos_bp.route("/<video_id>/rentals", methods =["GET"])
def rental_customers(video_id):
    video = is_parameter_found(Video, video_id)

    rentals = video.rentals
    
    customers_list = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        customers_list.append(
            {
        "due_date": str(rental.checkout_date + timedelta(days=7)),
        "name": customer.name,
        "phone": customer.phone,
        "postal_code": customer.postal_code,
            }
            )

    return jsonify(customers_list), 200
