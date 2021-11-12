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

# Get and Post Customers
@customer_bp.route("", methods=["POST", "GET"])
def handle_customers():
    if request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body:
            return jsonify({"details": "Request body must include name."}), 400 
        elif "postal_code" not in request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400
        elif "phone" not in request_body:
            return jsonify({"details": "Request body must include phone."}), 400
        
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"]
        )
        
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_dict()), 201

    elif request.method == "GET":
        customers=Customer.query.all()
        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_dict())
        return jsonify(customers_response), 200
        
# Get, Put, and Delete Customer by ID
@customer_bp.route("/<customer_id>", methods= ["GET", "PUT", "DELETE"])
def handle_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
            return jsonify({"Error": "Customer ID must be an integer."}), 400
    customer = Customer.query.get(customer_id)        
    if customer is None:
        return make_response({"message": f"Customer {customer_id} was not found"}), 404
    
    elif request.method == "GET":
        customer= Customer.query.get(customer_id)
        if customer is None:
            return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        return jsonify(customer.to_dict()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
            return jsonify({"details": "Request body must include name, phone, and postal code."}), 400
        customer.name=request_body["name"]
        customer.phone=request_body["phone"]
        customer.postal_code=request_body["postal_code"]
        db.session.commit()
        return jsonify(customer.to_dict()), 200

    elif request.method == "DELETE":
        customer_id=int(customer_id)
        customer=Customer.query.get(customer_id)
        db.session.delete(customer)
        db.session.commit()

        return({"id":customer_id}), 200

# Helper Function to validate videos
def validate_video(request_body):
    '''Helper Function to validate video request_body'''
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"details": "Request body must include title, release_date, and total_inventory."}), 400

# Get all Videos
@video_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200

# Post a Video
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body: 
        return jsonify({"details": "Request body must include title."}), 400
    elif "release_date" not in request_body:
        return jsonify({"details": "Request body must include release_date."}), 400
    elif "total_inventory" not in request_body:   
        return jsonify({"details": "Request body must include total_inventory."}), 400
    
    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201

# Get Video by ID
@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return jsonify({"Error": "Video ID must be an integer."}), 400

    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    return jsonify(video.to_dict()), 200

# Update Video by ID
@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    request_body = request.get_json()
    validated_video = validate_video(request_body)
    if validated_video is None:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    else: 
        return validated_video #Rename
    db.session.commit()
    return jsonify(video.to_dict()), 200

# Delete Video by ID
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": video.id}), 200

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
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    elif video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    if video.total_inventory == 0:
        return jsonify({"message": f"Video {video_id} is out of stock"}), 404
    
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

    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.to_dict()), 200