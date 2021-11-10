from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timezone
import requests
import os
from werkzeug.exceptions import NotFound


#DEFINE BLUEPRINTS
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#----------- HELPER FUNCTIONS -----------
def validate_video_id(video_id):
    try: 
        video_id == int(video_id)
    except:
        abort(400, {"message": f"video {video_id} was not found"})
    return Video.query.get_or_404(video_id)

def validate_customer_id(id):
    try: 
        id == int(id)
    except:
        abort(400, {"message": f"Customer {id} was not found"})
    return Customer.query.get_or_404(id)


#----------- CREATE ---------------------
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response(jsonify({"details" : "Request body must include title."}), 400)
    if "release_date" not in request_body:
        return make_response(jsonify({"details" : "Request body must include release_date."}), 400)
    if "total_inventory" not in request_body:
        return make_response(jsonify({"details" : "Request body must include total_inventory."}), 400)
    
    new_video = Video(
        title=request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
    )

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()),201)

@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return make_response(jsonify({"details" : "Request body must include name."}), 400)
    if "postal_code" not in request_body:
        return make_response(jsonify({"details" : "Request body must include postal_code."}), 400)
    if "phone" not in request_body:
        return make_response(jsonify({"details" : "Request body must include phone."}), 400)
    
    new_customer = Customer(
        name=request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(new_customer.to_dict()),201)

#----------- GET ---------------------
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response=[]
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    video = validate_video_id(id)
    request_body = request.get_json
    return jsonify(video.to_dict())

@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response=[]
    
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response)

@customer_bp.route("/<id>", methods=["GET"])
def get_one_customer(id):
    try:
        customer = validate_customer_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Customer {id} was not found"}),404)
    
    return jsonify(customer.to_dict())

#----------- UPDATE ---------------------

@customer_bp.route("/<id>", methods=["PUT"]) 
def update_customer(id):
    try:
        customer = validate_customer_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Customer {id} was not found"}),404)

    request_body = request.get_json()
    
    if request_body.get("name") and request_body.get("postal_code") and request_body.get("phone"): 
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    else:
        return make_response(jsonify({"message": f"attribute misson from video"}),400)
    
    db.session.commit()
    
    return customer.to_dict()

#----------- DELETE ---------------------

@customer_bp.route("/<id>", methods=["DELETE"]) 
def delete_customer(id):
    try:
        customer = validate_customer_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Customer {id} was not found"}),404)

    customer = customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    
    response_body = ({'id':customer.id, 'details': f'Customer {customer.id} successfully deleted'})
    return make_response(jsonify(response_body),200) 