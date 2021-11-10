from flask import Blueprint, jsonify, request, make_response, abort
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import date
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
def validate_customer_data(request_body):
    required_attributes = ["postal_code", "name", "phone"]

    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response({"details": f"Request body must include {attribute}."}, 400))

    return request_body

# create new customer
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = validate_customer_data(request.get_json())

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = date.today()
        )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

# get all customers
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)

# get, delete and update one customer
@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    
    if customer_id.isdigit():
        customer = Customer.query.get(customer_id)
        customer_id = int(customer_id)
    else:
        return make_response("", 400)
    
    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)

    elif request.method == "GET":
        return make_response(jsonify(customer.to_dict()), 200)

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return make_response(jsonify({"id": customer_id}), 200)

    elif request.method == "PUT":
        request_body = validate_customer_data(request.get_json())

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return make_response(jsonify(customer.to_dict()), 200)
