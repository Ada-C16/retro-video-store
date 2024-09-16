from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app import db
from datetime import date

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Helper Function to get Customer and Video IDs with specific customers and videos
def get_object_with_id(obj_type, obj_id):
    if obj_type == "video":
        obj = Video.query.get(obj_id)
    elif obj_type == "customer":
        obj = Customer.query.get(obj_id)
    else:
        abort(404)
    
    if obj is None:
        abort(404)
    return obj

# Helper Function to get IDs - We didn't use this but look at what we did!! :)
# def get_ids(customer_id, video_id):
#     customer = Customer.query.filter_by(id=customer_id).first()
#     video = Video.query.filter_by(id=video_id).first()
#     if customer is None or video is None:
#         abort(make_response(jsonify({"Error": "Info not found."}), 404))
#     return customer, video

def checkout_dict(video, customer):
    return {
        "video_id": video.video_id,
        "customer_id": customer.customer_id,
        "videos_checked_out_count": customer.get_rentals_count(),
        "available_inventory": video.get_available_inventory()
    }

# Nested Route for Rentals - Post checkout
@rental_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify({"Error": "Missing Customer ID or Video ID."}), 400
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    try:
        customer_id = int(customer_id)
        video_id = int(video_id)
    except ValueError:
        return jsonify({"Error": "Customer ID and Video ID must be integers."}), 400
    
    customer = get_object_with_id("customer", customer_id)
    video = get_object_with_id("video", video_id)

    if video.get_available_inventory() == 0:
        return jsonify({"message": "Could not perform checkout"}), 400
    
    new_rental = Rental(customer_id=customer_id, video_id=video_id)
    customer.rentals.append(new_rental)
    video.rentals.append(new_rental)
    
    db.session.commit()
    return jsonify(checkout_dict(video, customer)), 200

# Nested Route for Rentals - Post Checkin
@rental_bp.route("/check-in", methods=["POST"])
def checkin_video():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify({"Error": "Missing Customer ID or Video ID."}), 400
    
    customer_id = request_body["customer_id"]
    customer = get_object_with_id("customer", customer_id)
    video_id = request_body["video_id"]
    video = get_object_with_id("video", video_id)

    try:
        customer_id = int(customer_id)
        video_id = int(video_id)
    except ValueError:
        return jsonify({"Error": "Customer ID and Video ID must be integers."}), 400
    
    rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id).first()
    if rental is None:
        return jsonify({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}), 400
    db.session.delete(rental)
    db.session.commit()
    return jsonify(checkout_dict(video, customer)), 200