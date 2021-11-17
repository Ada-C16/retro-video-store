import os
import requests
from sqlalchemy.orm import query
from app import db
from datetime import datetime, timedelta
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

        def request_body_error(missing_field):
            return jsonify({"details": f"Request body must include {missing_field}."}), 400
        # probably don't need if you are only using it in one place and return in line 47 instead, make it global if it shows up more

        missing_field_list = ["title", "release_date", "total_inventory"]

        for word in missing_field_list:
            # instead of having the variable you could put the list in the line, think about readibility
            # optimize for readibility, written once, and read a lot of times, how a reader is interperting
            if word not in request_body:
                return request_body_error(word)

        # if "title" not in request_body:
        #     return jsonify({"details": "Request body must include title."}), 400
        # elif "release_date" not in request_body:
        #     return jsonify({"details": "Request body must include release_date."}), 400
        # elif "total_inventory" not in request_body:
        #     return jsonify({"details": "Request body must include total_inventory."}), 400

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

@customers_bp.route("", methods=["GET","POST"])
def active_customers():
    if request.method == 'GET':
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
                customer_dict = customer.customer_dict()
                customers_response.append(customer_dict)

        return jsonify(customers_response),200

    elif request.method == 'POST':
        cst_request_body = request.get_json()
        if "name" not in cst_request_body:
            return jsonify({"details": "Request body must include name."}), 400
        elif "postal_code" not in cst_request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400
        elif "phone" not in cst_request_body:
            return jsonify({"details": "Request body must include phone."}), 400
        
        new_customer = Customer(
            # id = cst_request_body["id"],
            name = cst_request_body["name"],
            phone = cst_request_body["phone"],
            postal_code = cst_request_body["postal_code"]
        )

        db.session.add(new_customer)
        db.session.commit()

        new_cst_response = new_customer.customer_dict()

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
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify(None), 400

        
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()

        response_body= customer.customer_dict()
        return jsonify(response_body),200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.id}), 200
######

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_for_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    elif request.method == "GET":
        # videos_customer_rented = Rental.query.filter(Rental.customer_id == customer_id, checked_out = True).count # only video rented by specific renter
        # videos_customer_rented = Rental.query.filter(Rental.customer_id == customer_id).count # only video rented by specific renter
        list_of_videos = []
        for rental in customer.rentals:
            video = Video.query.get(rental.video_id)
            response_body = {
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date,
            }
            list_of_videos.append(response_body)

        return jsonify(list_of_videos), 200
 #joins rental & video Rental.join(Video,Video.id == Rental.video_id) 



@videos_bp.route("/<video_id>/rentals", methods = ["GET"])
def get_videos_for_rental(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return jsonify (
            {"message": f"Video {video_id} was not found"}), 404
    elif request.method == 'GET':
        list_of_customers = []
        for rental in video.rentals:
            customer = Customer.query.get(rental.customer_id)
            response_body = {
                "due_date": rental.due_date,
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": customer.postal_code
            }
            list_of_customers.append(response_body)

        return jsonify(list_of_customers), 200


@rentals_bp.route("/check-out", methods = ["POST"])
def get_rental_check_out():
    request_body = request.get_json()

    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify(None), 400

    video = Video.query.get_or_404(request_body["video_id"])
    customer = Customer.query.get_or_404(request_body["customer_id"])

    videos_checked_out = Rental.query.filter_by(video_id=video.id, checked_out=True).count()
    # keyword argument and wouldn't have the space

    available_inventory = video.total_inventory - videos_checked_out

    if available_inventory == 0:
        return jsonify({
            "message": "Could not perform checkout"
        }), 400

    new_rental = Rental(
        video_id = video.id,
        customer_id = customer.id,
        due_date = datetime.now() + timedelta(days=7),
        checked_out=True
        # python - keyword argument passing through vs assignment, keyword argument to instate something or method, python convention
    )

    db.session.add(new_rental)
    db.session.commit()

    videos_checked_out = Rental.query.filter_by(customer_id=customer.id, checked_out=True).count()
    # specific customer and how many videos they have checked, better variable name
    # even though we are checking it again, checked out wouldn't be included since the informa, 

    if new_rental.checked_out is True:
        available_inventory -= 1

    return jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": datetime.now() + timedelta(days=7),
        "videos_checked_out_count": videos_checked_out,
        "available_inventory": available_inventory
}), 200


@rentals_bp.route("/check-in", methods = ["POST"])
def get_rental_check_in():
    request_body = request.get_json()

    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify(None), 400

    video = Video.query.get_or_404(request_body["video_id"])
    customer = Customer.query.get_or_404(request_body["customer_id"])
    # queries automatically add to the session/db so redundate to do it again
    
    number_of_rentals = Rental.query.filter_by(video_id = video.id, customer_id = customer.id, checked_out = True).count()
    videos_checked_out = Rental.query.filter_by(customer_id = customer.id, checked_out = True).count()

    if number_of_rentals == 0 or videos_checked_out == 0:
        return jsonify({
            "message": f"No outstanding rentals for customer {customer.id} and video {video.id}"
        }), 400

    rental = Rental.query.filter_by(video_id=video.id, customer_id=customer.id, checked_out=True).one()
    rental.checked_out = False

    db.session.commit()

    video_availablity = Rental.query.filter_by(video_id=video.id, checked_out=True).count()
    available_inventory = video.total_inventory - video_availablity
    videos_checked_out = Rental.query.filter_by(customer_id = customer.id, checked_out = True).count()

    return jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": videos_checked_out,
        "available_inventory": available_inventory
    }), 200