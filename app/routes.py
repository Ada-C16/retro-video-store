from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, date, timedelta
from app.models.video import Video
import requests, json
from dotenv import load_dotenv
import os
from app.models.utility_func import *
from app.models.rental import Rental


customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
video_bp = Blueprint("video", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@customer_bp.route("", methods=["GET"])
def get_all_customers():
    all_customers = Customer.query.all()

    if not all_customers:
        return jsonify([]), 200
    
    customers_list = [] 
    for customer in all_customers:
        customer_dict = {
            "id" : customer.id, 
            "name" : customer.name, 
            "postal_code" : customer.postal_code,
            "phone": customer.phone,
            "register_at" : customer.register_at
        }
        customers_list.append(customer_dict)
    
    return jsonify(customers_list), 200


@customer_bp.route("/<customer_id>", methods=["GET"])
def get_a_customer(customer_id):
    if not customer_id.isnumeric():
        return {'message': "Invalid type"}, 400

    try:
        customer = Customer.query.get(customer_id)

        return  {
        "id" : customer.id, 
        "name" : customer.name,   
        "postal_code" : customer.postal_code,
        "phone": customer.phone,
        "register_at" : customer.register_at
        }, 200

    except:
        return {'message': f"Customer {customer_id} was not found"}, 404

@customer_bp.route("", methods=["POST"])
def post_a_customer():
    request_body = request.get_json()

    try:
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
            register_at = datetime.now()
            )
        db.session.add(new_customer)
        db.session.commit()

        return {"id" : new_customer.id}, 201
    except KeyError as err:
        if "name" in err.args:
            return {"details" : f"Request body must include name."}, 400
        if "postal_code" in err.args:
            return {"details" : f"Request body must include postal_code."}, 400
        if "phone" in err.args:
            return {"details" : f"Request body must include phone."}, 400


@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_a_customer(customer_id):
    customer = Customer.query.get(customer_id)

    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.add(customer)
        db.session.commit()

        return {
            "id" : customer.id,
            "name" : customer.name,
            "postal_code" : customer.postal_code,
            "phone" : customer.phone
        },200
    except KeyError:
        return {'message': "Invalid type"}, 400
    except:
        return {"message": f"Customer {customer_id} was not found"},404
    

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404

    num_outstanding_rental_with_customer_id = Rental.query.filter_by(customer_id=customer_id, checked_out=True).count()
    #if num_outstanding_rental_with_customer_id:
        # return {"message" : f"Customer {customer_id} has outstanding rentals"}, 200

    db.session.delete(customer)
    db.session.commit()
    return {
        "id" : customer.id
    }, 200


@video_bp.route("", methods=["GET"])
def get_all_videos():
    all_videos = Video.query.all()

    if not all_videos:
        return jsonify([]), 200
    
    videos_list = [] 
    for video in all_videos:
        video_dict = {
            "id" : video.id, 
            "title" : video.title, 
            "release_date" : video.release_date,
            "total_inventory": video.total_inventory
        }
        videos_list.append(video_dict)
    
    return jsonify(videos_list), 200

@video_bp.route("/<video_id>", methods=["GET"])
def get_a_video(video_id):
    if not video_id.isnumeric():
        return {'message': "Invalid type"}, 400

    try:
        video = Video.query.get(video_id)

        return  {
            "id" : video.id, 
            "title" : video.title, 
            "release_date" : video.release_date,
            "total_inventory": video.total_inventory
        }, 200

    except:
        return {'message': f"Video {video_id} was not found"}, 404

@video_bp.route("", methods=["POST"])
def post_a_video():
    request_body = request.get_json()

    try:
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
            )
        db.session.add(new_video)
        db.session.commit()

        return  {
            "id" : new_video.id, 
            "title" : new_video.title, 
            "release_date" : new_video.release_date,
            "total_inventory": new_video.total_inventory
        }, 201

    except KeyError as err:
        if "title" in err.args:
            return {"details" : f"Request body must include title."}, 400
        if "release_date" in err.args:
            return {"details" : f"Request body must include release_date."}, 400
        if "total_inventory" in err.args:
            return {"details" : f"Request body must include total_inventory."}, 400


@video_bp.route("/<video_id>", methods=["PUT"])
def update_a_video(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()
    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

        db.session.add(video)
        db.session.commit()

        return  {
            "id" : video.id, 
            "title" : video.title, 
            "release_date" : video.release_date,
            "total_inventory": video.total_inventory
        }, 200
    except KeyError:
        return {'message': "Invalid type"}, 400
    except:
        return {"message": f"Video {video_id} was not found"}, 404
    

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_a_video(video_id):
    try:
        video = Video.query.get(video_id)
        if Rental.query.filter_by(video_id=video_id, checked_out=True).count() > 0:
            return {"message" : f"Video {video_id} has outstanding rentals"}, 200
        db.session.delete(video)
        db.session.commit()

        return {
            "id" : video.id
        }, 200
    except:
        return {"message": f"Video {video_id} was not found"}, 404


@rental_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()
    try: 
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
    except KeyError as err:
        if "customer_id" in err.args:
            return {"details" : "Missing customer_id"}, 400
        elif "video_id" in err.args:
            return {"details" : "Missing video_id"}, 400

    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    num_of_rental = Rental.query.filter_by(video_id = video_id).count()
    available_inventory = video.total_inventory - num_of_rental
    if available_inventory == 0:        
        return {"message" : "Could not perform checkout"}, 400
    due_date = datetime.today()+ timedelta(days=7)

    #   commit rental
    new_rental = Rental(customer_id=customer_id, video_id=video_id, due_date=due_date, checked_out=True)
    db.session.add(new_rental)
    db.session.commit()        

    return {
        "customer_id" : customer.id,
        "video_id" : video_id,
        "due_date" : due_date,
        "videos_checked_out_count" : Rental.query.filter_by(customer_id = customer_id, checked_out = True).count(), 
        "available_inventory" : video.total_inventory - Rental.query.filter_by(video_id = video_id, checked_out=True).count()
    }, 200

@rental_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json()
    try: 
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
    except KeyError as err:
        if "customer_id" in err.args:
            return {"details" : "Missing customer_id"}, 400
        elif "video_id" in err.args:
            return {"details" : "Missing video_id"}, 400
    # try: 
    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    # to check if the checked in has been checked out
    num_of_rental = Rental.query.filter_by(customer_id=customer_id, video_id = video_id, checked_out=True).count()
    if num_of_rental == 0:
        return {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400

    rental_record = Rental.query.filter_by(customer_id = customer_id, video_id=video_id, checked_out=True).first()
    rental_record.checked_out = False
    db.session.commit()

    return {
        "customer_id" : customer.id,
        "video_id" : video_id,
        "videos_checked_out_count" : Rental.query.filter_by(customer_id = customer_id, checked_out=True).count(),
        "available_inventory" : video.total_inventory - Rental.query.filter_by(video_id = video_id, checked_out=True).count()
    }, 200

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_currently_checked_out(customer_id):
    if not customer_id.isnumeric():
        return {'message': "Invalid type"}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"message" : f"Customer {customer_id} was not found"}, 404

    response_list = []
    rental_records = Rental.query.filter_by(customer_id = customer_id, checked_out=True)

    for rental in rental_records:
        video_id = rental.video_id
        video = Video.query.get(video_id)
        response_list.append({
            "release_date" : video.release_date,
            "title" : video.title,
            "due_date" : rental.due_date
        })
    return jsonify(response_list), 200

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def videos_currently_checked_out(video_id):
    if not video_id.isnumeric():
        return {'message': "Invalid type"}, 400
    video = Video.query.get(video_id)
    if not video:
        return {"message" : f"Video {video_id} was not found"}, 404

    response_list = []
    rental_records = Rental.query.filter_by(video_id = video_id)

    for rental in rental_records:
        customer_id = rental.customer_id
        customer = Customer.query.get(customer_id)
        response_list.append({
            "due_date" : rental.due_date,
            "name" : customer.name,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code
        })
    return jsonify(response_list), 200

