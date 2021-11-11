from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime
import os

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# VIDEO ROUTES
@videos_bp.route("", methods=["POST", "GET"])
def handle_videos():
    # POST REQUEST
    if request.method == "POST":
        video_request_body = request.get_json()
        
        if "title" not in video_request_body:
            return jsonify({"details": "Request body must include title."}), 400
        elif "release_date" not in video_request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        elif "total_inventory" not in video_request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400
    
        new_video = Video(
            title = video_request_body["title"],
            release_date = video_request_body["release_date"],
            total_inventory = video_request_body["total_inventory"]
        )

        db.session.add(new_video)
        db.session.commit()

        new_video_response = new_video.get_video_dict()

        return jsonify(new_video_response), 201   
    # GET REQUEST
    elif request.method == "GET":
        video_title_query = request.args.get("title")
        if video_title_query:
            videos = Video.query.filter(Video.title.contains(video_title_query))
        else:
            videos = Video.query.all()

        video_response = []
        for video in videos:
            video_response.append(video.get_video_dict())
        
        if video_response == []:
            return jsonify(video_response), 200

        return jsonify(video_response), 200

# GET, PUT, DELETE ONE VIDEO AT A TIME
@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_video_at_a_time(video_id):
    if not video_id.isnumeric():
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    if request.method == "GET":
        return jsonify(video.get_video_dict()), 200

    elif request.method == "PUT":
        video_update_request_body = request.get_json()

        if "title" not in video_update_request_body:
            return jsonify(None), 400
        
        video.title = video_update_request_body["title"],
        video.release_date = video_update_request_body["release_date"],
        video.total_inventory = video_update_request_body["total_inventory"]
            
        db.session.commit()

        updated_video_response = video.get_video_dict()

        return jsonify(updated_video_response), 200

    elif request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()

        video_delete_response = video.get_video_dict()
        
        print("********", video_delete_response), 200
        return jsonify(video_delete_response), 200

# CUSTOMER ROUTES
@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    # POST REQUEST
    if request.method == "POST":
        cust_request_body = request.get_json()

        if "name" not in cust_request_body:
            return jsonify({"details": "Request body must include name."}), 400
        elif "postal_code" not in cust_request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400
        elif "phone" not in cust_request_body:
            return jsonify({"details": "Request body must include phone."}), 400

        new_customer = Customer(
            name = cust_request_body["name"],
            postal_code = cust_request_body["postal_code"],
            phone = cust_request_body["phone"]
        )

        db.session.add(new_customer)
        db.session.commit()

        new_cust_response = new_customer.get_cust_dict()
        
        return jsonify(new_cust_response), 201
    # GET REQUEST
    elif request.method == "GET":
        customer_name_query = request.args.get("name")
        customer_postal_query = request.args.get("postal_code")
        
        if customer_name_query:
            customers = Customer.query.filter(Customer.name.contains(customer_name_query))
        elif customer_postal_query:
            customers = Customer.query.filter(Customer.postal_code.contains(customer_postal_query))
        else:
            customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            customers_response.append(customer.get_cust_dict())

        if customers_response == []:
            return jsonify(customers_response), 200

        return jsonify(customers_response), 200
    
# GET, PUT, DELETE ONE CUSTOMER AT A TIME
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer_at_a_time(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)
    
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    
    if request.method == "GET":
        return jsonify(customer.get_cust_dict()), 200 

    elif request.method == "PUT":
        put_request_body = request.get_json()

        if "name" not in put_request_body:
            return jsonify(None), 400

        customer.name = put_request_body["name"]
        customer.phone = put_request_body["phone"]
        customer.postal_code = put_request_body["postal_code"]

        db.session.commit()

        updated_customer_response = {
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

        return jsonify(updated_customer_response), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        if customer == []:
            cust_invalid_delete_response = {"message": f"Customer {customer_id} was not found"}

            return jsonify(cust_invalid_delete_response), 404
        else:
            cust_delete_response = customer.get_cust_dict()

            return jsonify(cust_delete_response), 200

@rentals_bp.route("/check-out", methods=["GET", "POST"])
def handle_rentals():
    rentals_request_body = request.get_json()
    if "customer_id" not in rentals_request_body or "video_id" not in rentals_request_body:
        return jsonify(None), 400

    if request.method == "POST":
        rentals = Rental(
            customer_id = rentals_request_body["customer_id"],
            video_id = rentals_request_body["video_id"]
        )

        db.session.add(rentals)
        db.session.commit()

        rental_receipt = {
        "customer_id": rentals.customer_id,
        "video_id": rentals.video_id,
        "due_date": rentals.due_date,
        "videos_checked_out_count": rentals.video_rental_count(),
        "available_inventory": rentals.video_inventory()
        }
        
        print("************")
        print(rental_receipt)

        return jsonify(rental_receipt), 200

    elif request.method == "GET":
        pass
