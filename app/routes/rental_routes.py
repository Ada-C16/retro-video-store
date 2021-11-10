from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check_out", methods=["POST"])
def rental_check_out():
    
    request_body = request.get_json()

    #CHECK FOR VALID INPUT TYPE HERE

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    new_rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"],due_date=datetime.now())


    db.session.add(new_rental)
    db.session.commit()

    video = Video.query.get(new_rental.video_id)

    available_inventory=video.available_inventory()

    customer = Customer.query.get(new_rental.customer_id)

    videos_checked_out_count = customer.videos_checked_out()

    response_body = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }
    return response_body, 201


@rentals_bp.route("/check_in", methods=["POST"])
def rental_check_in():
    
    request_body = request.get_json()

    #CHECK FOR VALID INPUT TYPE HERE

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    
    #for refactoring: a way to query with two numbers?
    
    rentals = Rental.query.order_by(Rental.customer_id).all()
    
    
    for rental in rentals:
        if rental.video_id == request_body["video_id"]:
            rental.checked_in = True
            rental = rental

    db.session.commit()

    video = Video.query.get(request_body["video_id"])

    available_inventory=video.available_inventory()

    customer = Customer.query.get(request_body["customer_id"])

    videos_checked_out_count = customer.videos_checked_out()

    response_body = {
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }

    return response_body, 201