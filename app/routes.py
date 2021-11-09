from flask import Blueprint, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
import requests
import os
from dotenv import load_dotenv

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)

# Customers Routes

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    customer_id = int(customer_id)

    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)
    elif request.method == "GET":
        return make_response(jsonify(customer.to_dict()), 200)
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return make_response(jsonify({"id": customer_id}), 200)
    elif request.method == "PUT":
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return make_response(jsonify(customer.to_dict()), 200)


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    required_attributes = ["postal_code", "name", "phone"]  # belongs in the Customer database

    for attribute in required_attributes:
        if attribute not in request_body:
            return make_response(jsonify({"details": f"Request body must include {attribute}."}), 400)

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = request_body["registered_at"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)
