
from flask import Blueprint, json, jsonify, request, make_response, Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models.video import Video
from .models.customer import Customer
from .models.rental import Rental
from app import db
from sqlalchemy import exc
from sqlalchemy.exc import DataError
# from sqlalchemy.sql.operators import custom_op
# import re
# from flask.blueprints import Blueprint

videos_bp = Blueprint("videos", __name__, url_prefix ="/videos")
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@videos_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    try: 
        video = Video.query.get(video_id)
        if video:
            return jsonify(video.to_dict()), 200
        else:
            return make_response({"message": f"Video {video_id} was not found"}), 404
    except DataError:
        return make_response({"message": "invalid video id, please enter number"}), 400


@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    elif "release_date" not in request_body: 
        return {"details": "Request body must include release_date."}, 400
    elif "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]
                    )
    db.session.add(new_video)
    db.session.commit()
    
    return make_response(new_video.to_dict()), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def change_data(video_id):
    video = Video.query.get(video_id)
    form_data = request.get_json()
    
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        return make_response({"message": "missing data"}), 400
    else:
        if video:
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]
            db.session.commit()
            return make_response({
                "title":video.title, "release_date":video.release_date, "total_inventory":video.total_inventory})
        else:
            return make_response({"message": "Video 1 was not found"}), 404

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video:
        db.session.delete(video)
        db.session.commit()
        return make_response({f"id": int(video_id)})
    else:
        return make_response({"message": "Video 1 was not found"}), 404


@customer_bp.route("", methods=["GET", "POST"])
def handle_customers():
    pass

    if request.method == "POST":
        
        request_body = request.get_json()

        input_error = Customer.check_input_fields(request_body)

        if input_error:
            return input_error

        new_customer = Customer.from_json(request_body)

        db.session.add(new_customer)
        db.session.commit()

        return new_customer.to_dict(), 201
        
    elif request.method == "GET":

        customers = Customer.query.all()

        return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route("/<cust_id>", methods=["GET", "PUT", "DELETE"])
def handle_customer(cust_id):

    id_error = Customer.validate_id(cust_id)

    if id_error:
        return id_error

    customer = Customer.query.get(cust_id)
    
    if request.method == "GET":
        
        return customer.to_dict(), 200

    elif request.method == "PUT":

        request_body = request.get_json()

        input_error = Customer.check_input_fields(request_body)

        if input_error:
            return input_error 

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return customer.to_dict(), 200

    elif request.method == "DELETE":
        
        db.session.delete(customer)
        db.session.commit()

        return {
            "id": customer.id,
            "status": "deleted"
        }

@rentals_bp.route("/check-out", methods=["POST"])
def handle_rental_checkout():

    request_body = request.get_json()

    # check request body fields
    if "customer_id" not in request_body or "video_id" not in request_body:
        return { "message" : "missing information "}, 400

    # validate customer id
    customer_id = request_body["customer_id"]
    customer_id_error = Customer.validate_id(customer_id)
    if customer_id_error:
        return customer_id_error

    # validate video id
    video_id = request_body["video_id"]
    video_id_error = Video.validate_id(video_id)
    if video_id_error:
        return video_id_error

    available_inventory = Rental.get_available_video_inventory(video_id)

    if available_inventory == 0:
        return { "message" : "Could not perform checkout"}, 400

    # create new rental
    new_rental = Rental.from_json(customer_id, video_id)

    db.session.add(new_rental)
    db.session.commit()

    return new_rental.to_dict_check_out(), 200

@customer_bp.route("/<cust_id>/rentals", methods=["GET"])
def handle_customer_rentals(cust_id):
    
    id_error = Customer.validate_id(cust_id)

    if id_error:
        return id_error

    rentals = Rental.query.filter_by(customer_id = cust_id)

    return jsonify([rental.to_dict_customer_rentals() for rental in rentals]), 200


@rentals_bp.route("/check-in", methods=["POST"])
def rental_checkin_update():
    request_body = request.get_json()
    #checks responsebody
    if "customer_id" not in request_body or "video_id" not in request_body:
        return { "message" : "missing information "}, 400

    #validate customer id
    customer_id = request_body["customer_id"]
    customer_id_error = Customer.validate_id(customer_id)
    if customer_id_error:
        return customer_id_error

    # validate video id
    video_id = request_body["video_id"]
    video_id_error = Video.validate_id(video_id)
    if video_id_error:
        return video_id_error

    #gets matching rentals
    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    rental = Rental.query.filter(Customer.id == customer.id)\
        .filter(Video.video_id == video.video_id).first()

    #checks if rental is not checked out by customer
    if rental is None:
        return jsonify({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}), 400

    #changes rental to false for checked in
    rental.checked_out = False
    db.session.commit()

    return rental.to_dict_check_in(), 200


@videos_bp.route("/<id>/rentals", methods=["GET"])
def gets_customers_by_rental(id):
    #Validates id
    video_id_error = Video.validate_id(id)
    if video_id_error:
        return video_id_error

    #gets/filters to get all videos 
    rentals = Rental.query.filter_by(video_id = id).all()
    rental_list = []

    for rental in rentals:
        rent = rental.to_dict()
        customer = Customer.query.get(rental.customer_id)
        rental_list.append({
            "due_date": rent["due_date"],
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        })
   
    return jsonify(rental_list), 200


@rentals_bp.route("", methods=["GET"])
def get_all_rentals():
    #gets all rentals in the database
    rentals = Rental.query.all()
    return jsonify([rental.to_dict_customer_rentals() for rental in rentals]), 200

