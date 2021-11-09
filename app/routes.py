from app import db 
from flask import Blueprint, jsonify, request, make_response 
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers",__name__,url_prefix = "/customers") # path that gives you access to resources/endpoint
videos_bp = Blueprint("videos",__name__,url_prefix = "/videos")

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