from flask import Blueprint, jsonify, make_response, request, abort
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app.routes.customer_routes import get_customer_from_id
from app.routes.video_routes import is_parameter_found
from app import db
from datetime import datetime, timezone, timedelta, date
import requests
import os

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rental_bp.route("/check-out", methods=["POST"])
def checkout_rental():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        abort(400, "Request body must include a customer_id and video_id")

    customer = get_customer_from_id(request_body["customer_id"])
    video = is_parameter_found(Video, request_body["video_id"])

    # if total inventory is empty (unsure if it's testing against 0 or None, couldn't tell on test)
    if video.total_inventory - len(video.rentals) == 0:
        abort(make_response({"message": "Could not perform checkout"}, 400))

    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        checkout_date=date.today()
    )

    db.session.add(new_rental)
    db.session.commit()

    # how many videos are checked out
    videos_checked_out_count = len(customer.rentals)
    available_inventory = video.total_inventory - len(video.rentals)

    print(new_rental.to_dict(videos_checked_out_count, available_inventory))
    return jsonify(new_rental.to_dict(videos_checked_out_count, available_inventory)), 200


@rental_bp.route("/check-in", methods=["POST"])
def checkin_rental():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        abort(400, "Request body must include a customer_id and video_id")

    customer = get_customer_from_id(request_body["customer_id"])
    video = is_parameter_found(Video, request_body["video_id"])

    # if video.rentals not in customer.rentals:
    #     abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

    rental_checkin = db.session.query(Rental).filter_by(customer_id=customer.id, video_id=video.id).first()
    if rental_checkin not in customer.rentals:
        abort(make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400))

    db.session.delete(rental_checkin)
    db.session.commit()

    videos_checked_out_count = len(customer.rentals)
    available_inventory = video.total_inventory - len(video.rentals)

    response_body = {
            "customer_id": customer.id,
            "video_id": video.id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory,
}
    print(response_body)
    return jsonify(response_body),200
    

