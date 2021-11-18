from flask import abort,Blueprint,jsonify,request,make_response
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import datetime
import requests, os
from dotenv import load_dotenv


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
load_dotenv()

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():

    if request.method == "GET":
        customers = Customer.query.all()
        response = [customer.to_dict() for customer in customers]
        return jsonify(response), 200

    elif request.method == "POST":
        customers = Customer.query.all()

        request_body = request.get_json()

        if "name" not in request_body or not isinstance(request_body["name"], str):
            return make_response({"details": "Request body must include name."}, 400) 
        
        elif "postal_code" not in request_body or not isinstance(request_body["postal_code"], str):
            return make_response({"details": "Request body must include postal_code."}, 400) 

        elif "phone" not in request_body or not isinstance(request_body["phone"], str):
            return make_response({"details": "Request body must include phone."}, 400) 
        else:
            new_customer = Customer(name=request_body["name"], phone=request_body["phone"], postal_code=request_body["postal_code"]) 

        db.session.add(new_customer)
        db.session.commit()
        return make_response({"id": new_customer.id}, 201)


def validate_endpoint_id(id):
    try:
        int(id)
    except:
        abort(make_response({f"details": "Endpoint must be an int."}, 400))

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    customer = Customer.query.get(customer_id)
    validate_endpoint_id(customer_id)

    if request.method == "GET":
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        # elif not isinstance(customer_id, int):
        #     return make_response({"message": f"{customer_id} is not a valid customer"}, 400)

        
        return make_response({customer.to_dict()}, 200)

    elif request.method == "DELETE":
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": int(customer_id)}, 200)

    if request.method == "PUT":
        request_body = request.get_json()
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)
        elif  "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        else:
            response_body = request.get_json()
        
        customer.name = response_body["name"]
        customer.phone = response_body["phone"]
        customer.postal_code = response_body["postal_code"]
    
        db.session.commit()
        return make_response({customer.to_dict()}, 200)


@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return jsonify(response_body), 200

@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    
    try:
        new_video = Video(title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"])
    except KeyError:
        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        if "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400    
        if "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201


# WAVE 2

@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    try:
        customer_id = int(request_body["customer_id"])
        video_id = int(request_body["video_id"])
    except ValueError:
        return jsonify({"Error": "Customer ID and Video ID must be integers."}), 400


    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    elif video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    if video.total_inventory == 0:
        return jsonify({"message": f"Video {video_id} is out of stock"}), 404

    if "customer_id" not in request_body: 
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    new_rental = Rental(customer_id=request_body["customer_id"],
        video_id=request_body["video_id"])
        # videos_checked_out_count=request_body["videos_checked_out_count"],
        # available_inventory=request_body["available_inventory"]) 


    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.to_dict()), 200


@rentals_bp.route("/check_in", methods=["POST"])
def handle_rentals():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    new_rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"],
    due_date=datetime.now())

    db.session.add(new_rental)
    db.session.commit()


    new_video = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": None,
            "available_inventory": None
        }
    return new_video, 201

@customers_bp.route("/<customer_id>/rentals")
def read_customer_rentals(id):
    customer = Customer.query.get(id)
    customer_rentals = Rental.query.filter(Rental.customer_id == id).all()

    response = []

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404

    for item in customer_rentals:
        response.append(item.rental_dict(item.video_id))

    return jsonify(response), 200

@videos_bp.route("/<video_id>/rentals")
def read_rentals_by_video(video_id):
    video = Video.query.get(video_id)
    video_rentals = Rental.query.filter(Rental.video_id == video_id).all()

    rentals_response = []    

    if not video:
        return {"message": f"Video {video_id} was not found"}, 404

    for item in video_rentals:
        id = item.customer_id
        rentals_response.append(item.get_rental_by_video(id))

    return jsonify(rentals_response), 200

