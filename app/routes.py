from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request
# from sqlalchemy import asc, desc
from datetime import datetime, date
from app.models.video import Video
import requests, json
from dotenv import load_dotenv
import os
from app.models.utility_func import *


customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

video_bp = Blueprint("video", __name__, url_prefix="/videos")

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
    try:
        customer = Customer.query.get(customer_id)

        db.session.delete(customer)
        db.session.commit()

        return {
            "id" : customer.id
        }, 200
    except:
        return {"message": f"Customer {customer_id} was not found"}, 404



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

        db.session.delete(video)
        db.session.commit()

        return {
            "id" : video.id
        }, 200
    except:
        return {"message": f"Video {video_id} was not found"}, 404

