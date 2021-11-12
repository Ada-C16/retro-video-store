from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()

    try:
        customer = Customer.query.get_or_404(request_body["customer_id"])
        video = Video.query.get_or_404(request_body["video_id"])
    except KeyError:
        return jsonify(None), 400

    if video.total_inventory - len(video.customers) == 0:
        return {"message": "Could not perform checkout"}, 400

    new_rental = Rental(
        customer_id = customer.id,
        video_id = video.id,
        due_date = datetime.now() + timedelta(days=7)
    )

    db.session.add(new_rental)
    db.session.commit()

    return jsonify(new_rental.to_dict())

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json()

    try:
        customer = Customer.query.get_or_404(request_body["customer_id"])
        video = Video.query.get_or_404(request_body["video_id"])
    except KeyError:
        return jsonify(None), 400

    rental = Rental.query.filter_by(customer_id = customer.id, video_id = video.id).first()

    rental.is_checked_in = True
    # customer.videos.remove(video)

    db.session.commit()

    return jsonify(rental.to_dict())