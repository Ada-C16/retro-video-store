from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, request, jsonify
from datetime import datetime
import os

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()

    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    # add video to customer's video list


    new_rental = Rental(
        customer_id = customer.id,
        video_id = video.id,
        due_date = datetime.datetime.now() + datetime.timedelta(days=7),
        # videos_checked_out_count = len(customer.videos),
        # videos_checked_out_count = len(video.customers),
        available_inventory = video.total_inventory - len(customer.videos)
    )