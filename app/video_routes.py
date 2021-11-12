from flask.wrappers import Response
from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort
import requests
import inspect
from flask_paginate import Pagination, get_page_parameter

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
    n = request.args.get("n")
    p = request.args.get("p")

    sort_query = request.args.get("sort")

    videos = Video.query.paginate(page=p, per_page=n, max_per_page=None)

    response_body = [video.to_dict() for video in videos.items]
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


# Custom endpoint for Wave 02

@videos_bp.route("/<id>/rentals", methods=["GET"])
def all_customers_for_checked_out_video(id):
    video = get_video_from_id(id)

    customer_list = []

    for customer in video.customers:
        rental_record = Rental.query.filter_by(video_id=id, customer_id=customer.id, return_date=None).first()
        customer_info = {
            "due_date": rental_record.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

        customer_list.append(customer_info)

    return jsonify(customer_list), 200


# WAVE 03 CUSTOM ENDPOINT

@videos_bp.route("/<id>/history", methods=["GET"])

def read_all_customers_with_checkout_video(id):
    video = get_video_from_id(id)

    past_rentals = Rental.query.filter(Rental.video_id==id, Rental.return_date!=None).all()

    customer_list = []

    for rental in past_rentals:
        customer = Customer.query.get(rental.customer_id)
        
        customer_data = {
            "customer_id" : customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": rental.checkout_date,
            "due_date": rental.due_date
        }

    return jsonify(customer_list),200