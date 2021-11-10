from flask import Blueprint, jsonify, request, make_response, abort
from app.models.video import Video
from app.models.customer import Customer
from app import db
from sqlalchemy import desc
from datetime import datetime
import requests
import os

# assign videos_bp to the new Blueprint instance
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# beginning CRUD routes/ endpoints for videos
@videos_bp.route("", methods=["POST"])
def post_one_video():
# request_body will be the user's input, converted to json. it will be a new record 
# for the db, with all fields (a dict)
    request_body = request.get_json()
# this guard clause will give an error if user tries to submit request body that does
# not have all fields present
    if 'title' not in request_body:
        return make_response({"details": "Request body must include title."}, 400)
    elif 'release_date' not in request_body:
        return make_response({"details": "Request body must include release_date."}, 400)
    elif 'total_inventory' not in request_body:
        return make_response({"details": "Request body must include total_inventory."}, 400)
    else:
# taking info fr request_body and converting it to new Video object    
        new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
# committing changes to db
        db.session.add(new_video)
        db.session.commit()
# return formatted response body
        return make_response({ "id": new_video.id,
                                        "title": new_video.title,
                                        "release_date": new_video.release_date,
                                        "total_inventory": new_video.total_inventory}, 201)

@videos_bp.route("", methods=["GET"])
def get_all_videos():
# querying db for all videos and ordering them by title, then storing that list of 
# objects in local videos variable    
    videos = Video.query.order_by(Video.title).all()
    videos_response = []
    # looping through eachvideo, converting to requested format (dict) and adding to
    # videos_response which will be list of dicts
    for video in videos:    
        videos_response.append({
        'id':video.id,
        'title':video.title,
        'release_date':video.release_date,
        'total_inventory':video.total_inventory
        })
    
    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def CRUD_one_video(video_id):
# this is a guard clause to make sure a video_id is an int, or can be converted to an int    
    try:
        int(video_id)
    except ValueError:
        return make_response({"details": "video_id must be valid integer"}, 400)
    video = Video.query.get(video_id) #either get Video back or None, video here is an object
    if video is None:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
# returning the object's info in the desired data structure format    
    if request.method == "GET":        
        return make_response({"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}, 200)
# PUT will replace the entire record with an entire new record, all fields
    elif request.method == "PUT":
    # form data is a local variable to hold the body of the HTTP request
        form_data = request.get_json()
# checking that form_data has all required fields
        if "title" not in form_data or "release_date" not in form_data \
        or "total_inventory" not in form_data:
            return make_response({"details": "all fields must be present"}, 400)

    # reassigning attributes of the video object using the dict values that came over 
    # in the request body
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return make_response({"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}, 200)
# PATCH will change just one part of the record, not the whole record
# not required but adding a patch for total_inventory on 11.9.21
    elif request.method == "PATCH":
        form_data = request.get_json()
        if "total_inventory" in form_data:
            video.total_inventory = form_data["total_inventory"]
        db.session.commit()
        return make_response({"video": {"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}}, 200)
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({'id': video.id}, 200)
        

# begin endpoints/ functions for Customer Model
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

def make_customer_dict(customer): 
    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone,
        "registered_at" : customer.registered_at,
        } 

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":       
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            current_customer = make_customer_dict(customer)
            customers_response.append(current_customer)
            
        return jsonify(customers_response), 200
    # POST
    else: 
        request_body = request.get_json()
        # if post is missing postal code, name, or phone number do not post and return 400
        if "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
        elif "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        # if all required values are given in the request body, return the video info with 201
        else: 
            new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()

        return make_customer_dict(new_customer), 201

@customers_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer(id):
    try:
        int_id = int(id)
    except ValueError:
        return jsonify(""), 400

    customer = Customer.query.get(id)
    
    # Guard clause 
    if customer is None:
        return jsonify({"message": (f'Customer {id} was not found')}), 404
    
    
    if request.method == "GET": 
        return jsonify(make_customer_dict(customer)), 200
        
    elif request.method == "PUT":
        form_data = request.get_json()
        if "postal_code" not in form_data or "phone" not in form_data or "name" not in form_data:
            return jsonify(""), 400

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()
        return jsonify(make_customer_dict(customer)), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({"id": customer.id}), 200
