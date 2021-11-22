from operator import itemgetter
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# Blueprints
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#Helper Functions
def is_id_valid(id):
    """Defined helper function to check the validity of the id"""
    try:
        int(id)
    except:
        abort(make_response(jsonify({"message": "Please input valid id number"}), 400))
    return id

def validate_data(request_body, required_attributes):
    """Defined helper function to validate the data passed in a request body"""
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {attribute}."}), 400))
    return request_body

def is_class_type_at_id_found(id, class_type, class_string):
    """Defined helper function to check if model instance exists"""
    id = is_id_valid(id)
    object= class_type.query.get(id)

    if not object:
        abort(make_response(jsonify({"message": f"{class_string} {id} was not found"}), 404))
    else:
        return object

def db_add(instance):
    """Defined helper function to add instance to database"""
    db.session.add(instance)
    db.session.commit()

def db_delete(instance):
    """Defined helper function to delete instance from database"""
    db.session.delete(instance)
    db.session.commit()
    
def handle_query_params(query_sort, query_page, query_limit, class_type, class_attribute):
    """Defined helper function to build and execute the query by chaining the appropriate commands"""
    list = class_type.query

    if query_sort == "desc":
        list = list.order_by(class_attribute.desc())
    elif query_sort == "asc":
        list = list.order_by(class_attribute)
    else:
        list = list.order_by(class_attribute)

    if query_limit:
        check_if_numeric(query_limit)
        list = list.limit(query_limit)

    if query_page:
        check_if_numeric(query_page)
        list = list.offset(int(query_limit)*int(query_page))
        
    else:
        list = list.all()

    return list

def check_if_numeric(thing_to_check):
    """Defined helper function if value is numeric"""

    if not thing_to_check.isnumeric():
        abort(make_response(jsonify({"message": f"Please use a number"})))
    else:
        return thing_to_check

#Videos Routes
@videos_bp.route("", methods=["GET", "POST"])
def handle_all_videos():
    """Defined endpoint to handle all HTTPS endpoints for handling video https request methods"""
    if request.method == "GET":
        query_sort = request.args.get("sort")
        query_limit = request.args.get("n")
        query_page = request.args.get("p")

        videos = handle_query_params(query_sort, query_page, query_limit, Video, Video.title)
        
        video_list = []
        for video in videos:
            video_list.append(video.to_dict())
        return make_response(jsonify(video_list), 200)

    elif request.method == "POST":
        required_attributes = ["title", "release_date", "total_inventory"]
        request_body = validate_data(request.get_json(), required_attributes)
        new_video = Video(title = request_body["title"],
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"]
                        )
        db_add(new_video)
        return make_response(jsonify(new_video.to_dict()), 201)

    else:
        return make_response(jsonify({"message": "http request method not permitted"}), 400)

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_video(video_id):
    """Defined endpoint to handle all specified video http request methods"""
    video = is_class_type_at_id_found(video_id, Video, "Video")

    if request.method == "GET":
        return make_response(jsonify(video.to_dict()), 200)
    
    elif request.method == "DELETE":
        if not video.rentals:
            db_delete(video)
            return make_response(jsonify({"id": int(video_id)}), 200)
        else:
            active_rentals = Rental.query.filter_by(video_id=f"{video.id}")
            for rental in active_rentals:
                db_delete(rental)
            db_delete(video)
            return make_response("", 200)
    
    elif request.method == "PUT":
        required_attributes = ["title", "release_date", "total_inventory"]
        request_body = validate_data(request.get_json(), required_attributes)
        video.title = request_body["title"]
        video.total_inventory = request_body["total_inventory"]
        video.release_date = request_body["release_date"]
        db.session.commit()
        return make_response(jsonify(video.to_dict()), 200)

    else:
        return make_response(jsonify({"message": "http request method not permitted"}), 400)

@videos_bp.route('/<video_id>/rentals', methods=["GET"])
def get_rentals_for_video(video_id):
    """Defined an endpoint for getting all rentals associated with a video"""
    video = is_class_type_at_id_found(video_id, Video, "Video")
    rentals = video.video_rentals() 
    return make_response(jsonify(rentals), 200)

# Customer Routes
@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    """Defined an endpoint to handle all customer http request methods"""
    if request.method == "GET":
        query_sort = request.args.get("sort")
        query_limit = request.args.get("n")
        query_page = request.args.get("p")

        customers = handle_query_params(query_sort, query_page, query_limit, Customer, Customer.name)

        customers_list = []
        for customer in customers:
            customers_list.append(customer.to_dict())
        return make_response(jsonify(customers_list), 200)

    elif request.method == "POST":
        required_attributes = ["postal_code", "name", "phone"]
        request_body = validate_data(request.get_json(), required_attributes)
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
            register_at = date.today()
            )
        db_add(new_customer)
        return make_response(new_customer.to_dict(), 201)
    
    else:
        return make_response(jsonify({"message": "http request method not permitted"}), 400)

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    """Defined an endpoint to handle all specified customer http request methods"""
    customer = is_class_type_at_id_found(customer_id, Customer, "Customer")

    if request.method == "GET":
        return make_response(jsonify(customer.to_dict()), 200)

    elif request.method == "DELETE":
        if not customer.rentals:
            db_delete(customer)
            return make_response(jsonify({"id": int(customer_id)}), 200)
        else:
            active_rentals = Rental.query.filter_by(customer_id=f"{customer.id}")
            for rental in active_rentals:
                db.session.delete(rental)
            db_delete(customer)
            return make_response("", 200)

    elif request.method == "PUT":
        required_attributes = ["postal_code", "name", "phone"]
        request_body = validate_data(request.get_json(), required_attributes)
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()
        return make_response(jsonify(customer.to_dict()), 200)
    
    else:
        return make_response(jsonify({"message": "http request method not permitted"}), 400)

@customers_bp.route('/<customer_id>/rentals', methods=["GET"])
def get_rentals_for_customer(customer_id):
    """Defined an endpoint for getting all rentals associated with a customer"""
    customer = is_class_type_at_id_found(customer_id, Customer, "Customer")
    rentals = customer.customer_rentals() 
    return make_response(jsonify(rentals), 200)

#Rental Routes
@rentals_bp.route("/<rental_status>", methods=["POST"])
def rental_status(rental_status):
    """Defined an endpoint for checking in and checking out a rental"""
    required_attributes = ["customer_id", "video_id"]
    request_body = validate_data(request.get_json(), required_attributes)

    customer = is_class_type_at_id_found(request_body["customer_id"], Customer, "Customer")
    video = is_class_type_at_id_found(request_body["video_id"], Video, "Video")

    rental = Rental(customer_id = int(customer.id),
                video_id = int(video.id),
                due_date = datetime.utcnow() + timedelta(days=7))

    if rental_status == "check-out":
        if video.total_inventory == 0:
            return make_response(jsonify({"message": "Could not perform checkout"}), 400)
        else:
            rental.rental_status(rental_status, video, customer)
            db_add(rental)
    
    elif rental_status == "check-in":
        if video.title not in customer.customer_rentals_titles():
            return make_response(jsonify({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}), 400)
        else:
            rental.rental_status(rental_status, video, customer)
            db.session.commit()

    else:
        return make_response(jsonify({"message": "http request method not permitted"}), 400)
        
    return make_response(jsonify(rental.to_dict(customer, video)), 200)