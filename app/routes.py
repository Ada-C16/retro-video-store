from app import db 
from flask import Blueprint, jsonify, request, make_response 
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers",__name__,url_prefix = "/customers") # path that gives you access to resources/endpoint
videos_bp = Blueprint("videos",__name__,url_prefix = "/videos")
rentals_bp = Blueprint("rentals",__name__,url_prefix = "/rentals")

@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body: 
            return jsonify({"details":"Request body must include title."}), 400
        if "release_date" not in request_body: 
            return jsonify({"details":"Request body must include release_date."}), 400
        if "total_inventory" not in request_body: 
            return jsonify({"details":"Request body must include total_inventory."}), 400
        else:
            new_video = Video(
            title= request_body["title"],
            release_date=request_body["release_date"],
            total_inventory =request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()
        new_video_response = {
                "id": new_video.id,
                "title" : new_video.title,
                "release_date": datetime.now(),
                "total_inventory": new_video.total_inventory
                }
        
        return jsonify(new_video_response), 201 

    
    elif request.method == "GET":

        videos_table = Video.query.all() # searching for all the videos in the videos table
        videos_list_response = [] # empty list 
        # if videos_table is None:
        #     return jsonify (videos_list), 200
            

        print(videos_table)
        for each_video in videos_table:
                videos_list_response.append(
                {

                    "id": each_video.id,
                    "title": each_video.title,
                    "release_date": each_video.release_date,
                    "total_inventory": each_video.total_inventory

                }
            )
        print (videos_list_response)
        return jsonify(videos_list_response), 200

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_video(video_id):
    if video_id.isnumeric() != True:
        return {"details" : "Invalid request"}, 400
    video = Video.query.get(video_id)
    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    elif request.method == "GET":
        return {
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }, 200
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({"id": video.id}), 200
    elif request.method == "PUT":
        form_data = request.get_json()
        if "title" not in form_data:
            return {"details" : "Invalid data"}, 400 
        else:
            video.title = form_data["title"]
            video.total_inventory = form_data["total_inventory"]
            video.release_date = form_data["release_date"]

            db.session.commit()

            return {"title" : video.title, "total_inventory" : video.total_inventory}, 200 

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":
        customers_database = Customer.query.all() # searching for all the customers in the database 
        customers_list = [] # empty list 
        for each_customer in customers_database:
                customers_list.append(
                    {
                    "name": each_customer.name,
                    "id" : each_customer.id,
                    "phone" : each_customer.phone,
                    "registered_at" : each_customer.registered_at,
                    "postal_code": each_customer.postal_code
                })
        return jsonify(customers_list), 200 

    elif request.method == "POST": 
        request_body = request.get_json()
        if "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        if "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        if "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
        else:
            new_customer = Customer(
                name= request_body["name"],
                phone=request_body["phone"],
                postal_code =request_body["postal_code"])

            db.session.add(new_customer)
            db.session.commit()
            new_customer_response = {
                    "id": new_customer.id,
                    "name" : new_customer.name,
                    "phone": new_customer.phone,
                    "registered_at": new_customer.registered_at,
                    "postal_code": new_customer.postal_code
                    }
            return jsonify (new_customer_response), 201

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    if customer_id.isnumeric() != True:
        return("Invalid Request"), 400
    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404
    elif request.method == "GET":
        return {
            "id": customer.id,
            "name" : customer.name,
            "registered_at" : customer.registered_at,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code
        }, 200
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({"id": customer.id}), 200
    elif request.method == "PUT":
        form_data = request.get_json()
        if "name" not in form_data:
            return {"details" : "Invalid data"}, 400 
    
        customer.name = form_data["name"]
        customer.phone = form_data["phone"]
        customer.postal_code = form_data["postal_code"]

        db.session.commit()

        return {"name" : customer.name, "phone" : customer.phone, "postal_code": customer.postal_code}, 200

def due_date():
    due_date =datetime.today() + timedelta(days=7)
    return due_date
    

@rentals_bp.route("/check-out", methods=["POST"])
def handle_checkout():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400
    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404
        
    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404
    movie_due = due_date()
    if video.total_inventory - Rental.query.filter_by(video_id=video_id).count() == 0:
        return {"message": "Could not perform checkout"}, 400
    rental= Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"],
        due_date = movie_due)

    db.session.add(rental)
    db.session.commit()
    rentals = Rental.query.filter_by(video_id=video_id).count()
    customers_rentals = customer.video

    checked_out = {
                    "video_id": rental.video_id,
                    "customer_id" : rental.customer_id,
                    "due_date": movie_due,
                    "available_inventory": video.total_inventory - rentals,
                    "videos_checked_out_count": len(customers_rentals)
                    }

    
        
                
        
    return jsonify (checked_out), 200


        
                    


@rentals_bp.route("/check-in", methods = ["POST"])
def handle_checkin_rental():

    request_body = request.get_json()
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404
    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404
    if customer_id == False:
        return 404
    movie_due = due_date()

    
    rental = Rental (
            customer_id = customer.id,
            video_id = video.id,
            )
    # Rental.query.get(rental).delete()

    # db.session.add(rental)
    # db.session.commit()

    rentals = Rental.query.filter_by(video_id=video_id).count()
    customers_rentals = video.customer
    customers_rentals=Rental.query.filter_by(id=video_id).count()
    if customers_rentals == 0:
        return{"message": "No outstanding rentals for customer 1 and video 1"}, 400

    checked_in = {
                    "video_id": rental.video_id,
                    "customer_id" : rental.customer_id,
                    "due_date": movie_due,
                    "available_inventory": video.total_inventory,
                    "videos_checked_out_count": (customers_rentals - rentals)}

    return jsonify(checked_in), 200

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customer_checkout(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message" : "Customer 1 was not found"}, 404
    customers_rentals = customer.video
    
    rentals = []
    for movie in customers_rentals:
        rental = Rental.query.filter_by(video_id=movie.id, customer_id=customer_id).first()
        rental_due_date = rental.due_date
        rentals.append({
            "release_date": movie.release_date,
            "title" : movie.title,
            "due_date": rental_due_date
            })
    if rentals is None:
        return jsonify(rental), 200
    return jsonify(rentals), 200 

    
