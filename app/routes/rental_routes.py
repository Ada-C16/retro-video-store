from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
import requests
from datetime import datetime, timedelta


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_vid():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response("", 400)

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video is None or customer is None:
        return jsonify(""), 404

    num_current_checked_out = Rental.query.filter_by(
        video_id=video.video_id, videos_checked_in=False).count()
    current_available_inventory = video.total_inventory - num_current_checked_out

    if current_available_inventory == 0:
        return jsonify({
            "message": "Could not perform checkout"
        }), 400

    new_rental = Rental(customer_id=customer.customer_id,
                        video_id=video.video_id,
                        due_date=(datetime.now() + timedelta(days=7)))

    db.session.add(new_rental)
    db.session.commit()

    num_videos_checked_out = Rental.query.filter_by(
        video_id=video.video_id, videos_checked_in=False).count()  # .count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(
        customer_id=customer.customer_id, videos_checked_in=False).count()

    response_body = {
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory
    }
    return jsonify(response_body), 200


@rentals_bp.route("/check-in", methods=["POST"])
def check_in_vid():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response("", 400)

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video is None or customer is None:
        return jsonify(""), 404

    rental = Rental.query.filter_by(
        video_id=video.video_id, customer_id=customer.customer_id, videos_checked_in=False).first()

    if rental is None:
        return jsonify({"message": f"No outstanding rentals for customer {customer.customer_id} and video {video.video_id}"}), 400

    rental.videos_checked_in = True

    num_videos_checked_out = Rental.query.filter_by(
        video_id=video.video_id, videos_checked_in=False).count()  # .count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(
        customer_id=customer.customer_id, videos_checked_in=False).count()

    db.session.commit()
    response_body = {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,

        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory
    }
    return jsonify(response_body), 200
