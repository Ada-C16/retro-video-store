
from marshmallow import schema
from app import db
from app.models.video import Video
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request, abort

from datetime import date 
import datetime, requests, os

from dotenv import load_dotenv

load_dotenv()


video_bp = Blueprint("videos", __name__, url_prefix="/videos")
from app.models.video import PutVideoInputSchema
put_video_schema = PutVideoInputSchema()

@video_bp.route("", methods=["POST"])
def create_video():
    request_data=request.get_json()
    # not_field=put_video_schema.validate(request.form)
    if "title" not in request_data: 
        invalid_data={"details": "Request body must include title."}
        return jsonify(invalid_data),400
    elif "release_date" not in request_data:
        invalid_data={"details": "Request body must include release_date."}
        return jsonify(invalid_data),400
    elif "total_inventory" not in request_data:
        invalid_data={"details": "Request body must include total_inventory."}
        return jsonify(invalid_data),400
    new_video=Video(title=request_data["title"], release_date=request_data["release_date"], total_inventory=request_data["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos_response = []
    videos = Video.query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200



@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404
    # if request.method=="GET":
    return jsonify({"title": video.title, "id": video.id, "total_inventory": video.total_inventory}), 200
    

@video_bp.route("/<id>", methods=["PUT"])
def put_one_video(id): 
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404   
    request_data=request.get_json()
    errors = put_video_schema.validate(request_data)
    if errors:
    # if "title" not in request_data: 
    #     invalid_data={"details": "Request body must include title."}
    #     return jsonify(invalid_data),400
    # elif "release_date" not in request_data:
    #     invalid_data={"details": "Request body must include release_date."}
    #     return jsonify(invalid_data),400
    # elif "total_inventory" not in request_data:
    #     invalid_data={"details": "Request body must include total_inventory."}
    #     return jsonify(invalid_data),400
        return jsonify({"details": f"{errors} Invalid data"}),400
    else:
        video.title=request_data["title"]
        video.release_date=request_data["release_date"]
        video.total_inventory=request_data["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()),200

@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    id=validate_id_int(id)
    
    video = Video.query.get(id)

    if video:
        db.session.delete(video)
        db.session.commit()
        return {"id": video.id}, 200
    else:
        return {"message":f"Video {id} was not found"}, 404

def validate_id_int(id):
    try:
        id = int(id)
        return (id)
    except:
        abort(400, "Error: id needs to be a number")


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# creates a customer
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(
        new_customer.to_dict(), 201
    )

# lists all existing customers and details about each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []
    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# gets details about a specific customer
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400
        
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    return make_response(
        customer.to_dict(), 200
    )

# updates and return details about a specific customer
# NOT PASSING
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return jsonify({
        "name": f"{customer.name}",
        "phone": f"{customer.phone}",
        "postal_code": f"{customer.postal_code}"
        }        
    )
    

# deletes a specific customer
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    db.session.delete(customer)
    db.session.commit()

    return make_response(
        {"id": customer.id}, 200
    )

    # return {"id": customer.id}, 200

