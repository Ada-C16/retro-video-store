from flask import Blueprint, jsonify, request, make_response, abort
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import date, timedelta
import requests
from dotenv import load_dotenv

# Blueprints
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#Videos routes

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)


@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):

    video_id = is_id_valid(video_id)
    video = Video.query.get(video_id)

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 
    else:
        return make_response(jsonify(video.to_dict()), 200)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 
    else:
        db.session.delete(video)
        db.session.commit()
        return make_response(jsonify({"id": int(video_id)}), 200)

@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = video_has_required_attributes(request.get_json())

    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"]    
)
    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    request_body = video_has_required_attributes(request.get_json())

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    db.session.commit()

    return make_response(jsonify(video.to_dict()), 200)


# customer routes
# create new customer
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = validate_customer_data(request.get_json())

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = date.today()
        )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

# get all customers
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)

# get, delete and update one customer
@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    
    customer_id = is_id_valid(customer_id)
    customer = Customer.query.get(customer_id)
    customer_id = int(customer_id)

    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)

    elif request.method == "GET":
        return make_response(jsonify(customer.to_dict()), 200)

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return make_response(jsonify({"id": customer_id}), 200)

    elif request.method == "PUT":
        request_body = validate_customer_data(request.get_json())

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return make_response(jsonify(customer.to_dict()), 200)

#Helper Functions

def is_id_valid(video_id):
    try:
        int(video_id)
    except:
        abort(make_response(jsonify({"message": "Please input valid id number"}), 400))
    return video_id

def video_has_required_attributes(request_body):
    required_attributes = ["title", "release_date", "total_inventory"]
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {attribute}."}), 400))
    return request_body

def validate_customer_data(request_body):
    required_attributes = ["postal_code", "name", "phone"]
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response({"details": f"Request body must include {attribute}."}, 400))

    return request_body

#Rental Endpoints
@rentals_bp.route("/<rental_status>", methods=["POST"])
def rental_status(rental_status):
    request_body = request.get_json()
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    if not customer or not video:
        return make_response("", 404)

    if rental_status == "check-out":
        video.total_inventory -= 1
        if customer.number_of_rentals == None:
            customer.number_of_rentals = 0
            customer.number_of_rentals += 1
        else:
            customer.number_of_rentals += 1
            
        rental = Rental(customer_id = request_body["customer_id"],
                        video_id = request_body["video_id"],
                        due_date = date.today() + timedelta(days=7))
        dict_rent = rental.to_dict()
        dict_rent["videos_checked_out_count"] = customer.number_of_rentals
        dict_rent["available_inventory"] = video.total_inventory
    
    return make_response(jsonify(dict_rent), 200)