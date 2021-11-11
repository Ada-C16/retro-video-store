from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from flask_sqlalchemy import model
from sqlalchemy import func
import requests
from datetime import timedelta, datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def handle_rentals():
    request_body=request.get_json()
    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return make_response({"message":"Could not perform checkout"}, 404)
    elif not video:
        return make_response({"message":"Could not perform checkout"}, 404)


    new_rental = Rental(
            customer_id=request_body["customer_id"],
            video_id=request_body["video_id"]
            )
    db.session.add(new_rental)
    db.session.commit()


    rentals_per_customer = len(customer.rentals)
    available_rentals_per_video= video.available_rentals - rentals_per_customer

    response_value = {"customer_id":new_rental.customer_id,
        "video_id":new_rental.video_id,
        "due_date": datetime.now + timedelta(days=7),
        "videos_checked_out_count": rentals_per_customer,
        "available_inventory": available_rentals_per_video}

    return make_response(response_value, 201)