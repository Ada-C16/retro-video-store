import re
from app import db
from app.models.customer import Customer
from datetime import date
from app.models.rental import Rental
from app.models.video import Video
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request


rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rental_bp.route("/check-out", methods=["POST"])
def rental_check_out():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return jsonify(None), 400
    if "video_id" not in request_body:
        return jsonify(None), 404

    # to - do make a rental and commit
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    count_of_rentals = len(video.rentals)
    count_customer_rentals = len(customer.rentals)

    video_avialable_inventory = video.total_inventory - count_of_rentals
    today = datetime.today()
    due_date = today + datetime.timedelta(days=7)

    response_body = {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": due_date,
        "videos_checked_out_count": count_customer_rentals,
        "available_inventory": video_avialable_inventory,
    }

    return jsonify(response_body), 200


@rental_bp.route("/check-in", methods=["POST"])
def rental_check_in():
    pass
