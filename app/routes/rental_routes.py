from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app import db
from datetime import date
import requests, os
from dotenv import load_dotenv

video_bp = Blueprint("video", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")
load_dotenv()

# Nested Route for Rentals - Post checkout
@video_bp.route("/check-out", methods=["POST"])
def create_rental(self, customer_id, video_id):
    try:
        customer_id = int(customer_id)
        video_id = int(video_id)
    except ValueError:
        return jsonify({"Error": "Customer ID and Video ID must be integers."}), 400

    request_body = request.get_json()
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    
    if "customer_id" not in request_body: 
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    new_rental = Rental(
        customer_id=customer_id,
        video_id=video_id,
        videos_checked_out_count = self.videos_checked_out_count,
        available_inventory = self.available_inventory
    )

    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    elif video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    elif video.total_inventory == 0:
        return jsonify({"message": f"Video {video_id} is out of stock"}), 404
    
    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.to_dict()), 200