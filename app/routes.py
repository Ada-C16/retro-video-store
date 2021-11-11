import os
import requests
from sqlalchemy.orm import query
from app import db
from datetime import datetime
from dotenv import load_dotenv
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from flask import Blueprint, json, jsonify, request

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@videos_bp.route("", methods = ["GET", "POST"])

def handle_videos():
    videos = Video.query.all()

    if videos is None:
        return jsonify([]), 200

    elif request.method == "GET":
        videos_list = []
        for video in videos:
            videos_list.append({
                "id": video.id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            })
        
        return jsonify(videos_list), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        elif "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        elif "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400

        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )

        db.session.add(new_video)
        db.session.commit()

        return jsonify({
            "id": new_video.id,
            "title": new_video.title,
            "release_date": new_video.release_date,
            "total_inventory": new_video.total_inventory
        }), 201

@videos_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def handle_video_id(video_id):

    if video_id.isnumeric() is False:
        return jsonify(None), 400
    
    video = Video.query.get(video_id)
    # video = Video.query.get_or_404(video_id), gives a 404 error ahead of time and a response body of None

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    elif request.method == "GET":
        return jsonify({
                "id": video.id,
                "title": video.title,
                "total_inventory": video.total_inventory
        }), 200
    
    elif request.method == "PUT":
        updated_body = request.get_json()

        if "title" not in updated_body or "release_date" not in updated_body or "total_inventory" not in updated_body:
            return jsonify(None), 400

        video.title = updated_body["title"]
        video.release_date = updated_body["release_date"]
        video.total_inventory = updated_body["total_inventory"]
        db.session.commit()

        return jsonify({
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        })

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({"id": video.id}), 200


@videos_bp.route("/<video_id>/rentals", methods = ["GET"])


@rentals_bp.route("/check-out", methods = ["POST"])

@rentals_bp.route("/check-in", methods = ["POST"])
@customers_bp.route("", methods=["GET","POST"])
def active_customers():
    if request.method == 'GET':
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            # customers_response.append(
                customer_dict = customer.customer_dict()
                customers_response.append(customer_dict)

        return jsonify(customers_response),200

    elif request.method == 'POST':
        cst_request_body = request.get_json()
        if "name" not in cst_request_body or "postal_code" not in cst_request_body or "phone" not in cst_request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400

        new_customer = Customer(
            name = cst_request_body["name"],
            postal_code = cst_request_body["postal_code"],
            phone = cst_request_body["phone"]
        )

        db.session.add(new_customer)
        db.session.commit()

        new_cst_response = {"The phone number you provide must be 10 digits.":new_customer.customer_dict()}

        return jsonify(new_cst_response),201

@customers_bp.route("/<customer_id>", methods =["GET", "PUT", "DELETE"])
def retrieve_customer(customer_id):
    if customer_id.isdigit() is False:
        return jsonify(None), 400
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify({"message": "Customer 1 was not found"}), 404
    elif request.method == 'GET':
        response_body  = customer.customer_dict()
        return jsonify(response_body), 200

    elif request.method == 'PUT':
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone_ = request_body["phone"]
        db.session.commit()

        response_body={"customer":(customer.customer_dict())}
        return jsonify(response_body),200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify({f"message": "Customer {customer.id} was not found"}),200
