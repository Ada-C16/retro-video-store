from app import db
from app.models.customer import Customer 
from flask import Blueprint, jsonify, request
import os
from datetime import datetime

from app.models.video import Video


# Blueprints
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# Customer helper functions
def display_customer_info(customer):
    return {
        "id": customer.id,
        "name": customer.name,
        "postal_code": customer.postal_code,
        "phone": customer.phone
    }

def customer_not_found(customer_id):
    return {"message" : f"Customer {customer_id} was not found"}

# customers endpoint

# returns list of all existing customers
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    if customers is None:
        return jsonify("Not Found"), 404

    customer_response = []
    for customer in customers:
        customer_response.append({
            "id": customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone})


    return jsonify(customer_response), 200


# returns one instance of a specific customer 
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400
    
    customer = Customer.query.get(customer_id)

    if customer == None:
        response_body = {"message" : f"Customer {customer_id} was not found"}
        return jsonify(response_body), 404
    
    response_body = {"id": customer.id, "name": customer.name, "postal_code": customer.postal_code, "phone": customer.phone}

    return jsonify(response_body), 200


# creates a new customer
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    if "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    if "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
        )

    db.session.add(new_customer)
    db.session.commit()

    return ({
        "id": new_customer.id,
        "name": new_customer.name,
        "postal_code": new_customer.postal_code,
        "phone": new_customer.phone
    }), 201


# updates an exsiting customers record
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_existing_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id), 404


    request_body = request.get_json()
    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        return jsonify("Bad Request"), 400

    customer.name = request_body.get("name")
    customer.postal_code = request_body.get("postal_code")
    customer.phone = request_body.get("phone")
    customer.registered_at = datetime.now()

    db.session.commit()
    response_body = ({
            "name": f"{customer.name}",
            "postal_code": f"{customer.postal_code}",
            "phone": f"{customer.phone}"})

    return response_body, 200


# delete an exsiting customer record
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_existing_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id), 404

    db.session.delete(customer)
    db.session.commit()

    return {
        "id": customer.id
        }, 200


# *****************************
# *** videos endpoint  CRUD ***
# *****************************

# READ
# get all existing video records
@videos_bp.route("", methods = ["GET"])
def get_videos():
    videos = Video.query.all()
    
    if videos == None:
        return [], 200

    response_body = [video.to_dict() for video in videos]

    return jsonify(response_body), 200

# get one video record via id number
@videos_bp.route("/<video_id>", methods = ["GET"])
def get_video(video_id):

    # check that </video_id> is valid input (ie an id number)
    if not video_id.isnumeric():
        return jsonify(None), 400
    
    video = Video.query.get(video_id)
    
    if video == None:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    response_body = video.to_dict()

    return jsonify(response_body), 200

# CREATE
# post a video record
@videos_bp.route("", methods = ["POST"])
def post_video():
    request_body = request.get_json()

    if "title" not in request_body:
        response_body = {"details": "Request body must include title."}
        return jsonify(response_body), 400
    elif "release_date" not in request_body:
        response_body = {"details": "Request body must include release_date."}
        return jsonify(response_body), 400
    elif "total_inventory" not in request_body:
        response_body = {"details": "Request body must include total_inventory."}
        return jsonify(response_body), 400

    new_video = Video.from_dict(request_body)

    db.session.add(new_video)
    db.session.commit()

    response_body = new_video.to_dict()

    return jsonify(response_body), 201

# UPDATE
# update a video record
@videos_bp.route("<video_id>", methods = ["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    
    if video is None:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    form_data = request.get_json()
    
    if "title" not in form_data or "total_inventory" not in form_data or "release_date" not in form_data:
        return jsonify(None), 400

    video.title = form_data["title"]
    video.total_inventory = form_data["total_inventory"]
    video.release_date = form_data["release_date"]

    db.session.commit()

    response_body = video.to_dict()

    return jsonify(response_body), 200


# DELETE
# delete a video record
@videos_bp.route("/<video_id>", methods = ["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        response_body = {"message": f"Video {video_id} was not found"}
        return jsonify(response_body), 404
    else:
        response_body = {"id" : video.id}

        db.session.delete(video)
        db.session.commit()

        return jsonify(response_body), 200

# *****************************
# *** POST custom endpoints ***
# *****************************

# POST /rentals/check-out
# *** QUESTION: DO WE NEED TO MAKE A NEW BLUEPRINT FOR RENTALS? ***
@videos_bp.route("/rentals/check-out", methods = ["POST"])
def post_rentals_check_out(customer_id, video_id):
    request_body = request.get_json()
    
    # check for valid input
    if "customer_id" not in request_body:
        response_body = {"details": "Request body must include customer_id."}
        return jsonify(response_body), 400
    elif "video_id" not in request_body:
        response_body = {"details": "Request body must include video_id."}
        return jsonify(response_body), 400

    # check if customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id), 404

    #check if video exists
    video = Video.query.get(video_id)
    if not video:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    # create a response body
    response_body = {}

    return jsonify(response_body), 201


# POST /rentals/check-in
@videos_bp.route("/rentals/check-in", methods = ["POST"])
def post_rentals_check_in():
    request_body = request.get_json()
    response_body = {}
    return jsonify(response_body), 201
