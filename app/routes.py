from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from dotenv import load_dotenv
import os
from sqlalchemy import desc
from datetime import date
from datetime import timedelta
# import datetime




customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")


def validate_id_int(id):
    try:
        id = int(id)
        return id
    except:
        abort(400, "Error: ID needs to be a number.")

def validate_customer_request_body(request_body):
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400
    return False

def validate_video_request_body(request_body):
    if "title" not in request_body:
        return jsonify({"details": "Request body must include title."}), 400
    if "release_date" not in request_body:
        return jsonify({"details": "Request body must include release_date."}), 400
    if "total_inventory" not in request_body:
        return jsonify({"details": "Request body must include total_inventory."}), 400
    return False

# ---------------------------
# ------- CUSTOMERS ---------
# ---------------------------

# Posts new customer
@customers_bp.route("", methods = ["POST"])
def create_customer():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_customer_request_body(request_body)
    if invalid:
        # Returns the invalid error message and status code
        return invalid
        
    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()

    new_customer_response = new_customer.to_dict()
    return jsonify(new_customer_response), 201

# Handles all customers
@customers_bp.route("", methods=["GET"])
def handle_customers():
    customers_response = []
    sort_by = request.args.get('sort')
    # Poss. Refactor: Could make a helper function, passing in sort_by as parameter
    if sort_by == "asc":
        customers = Customer.query.order_by(Customer.name).all()
    elif sort_by == "desc":
        customers = Customer.query.order_by(desc(Customer.title)).all()
    else:
        customers = Customer.query.all()
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# Handles one customer
@customers_bp.route("/<id>", methods=["GET", "PUT"])
def handle_customer(id):
    id = validate_id_int(id)
    customer = Customer.query.get(id)
    if not customer:
        return make_response({"message": f"Customer {id} was not found"}, 404)
    if request.method == "GET":
        return jsonify(customer.to_dict()), 200
    elif request.method == "PUT":
        request_body = request.get_json()
        # Check if request_body is invalid/missing data
        invalid = validate_customer_request_body(request_body)
        if invalid:
            # Returns the invalid error message and status code
            return invalid

        customer.name=request_body["name"]
        customer.postal_code=request_body["postal_code"]
        customer.phone=request_body["phone"]

        db.session.commit()
        return jsonify(customer.to_dict()), 200

# Deletes one customer
@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    #print(id)
    id=validate_id_int(id)
    
    customer = Customer.query.get(id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": id}, 200)
    else:
        return make_response({"message": f"Customer {id} was not found"}, 404)

# ---------------------------
# --------- VIDEOS ----------
# ---------------------------

# Handles all videos
@videos_bp.route("", methods = ["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        sort_by = request.args.get('sort')
        if sort_by == 'asc':
            videos = Video.query.order_by(Video.title).all()
        elif sort_by == 'desc':
            videos = Video.query.order_by(desc(Video.title)).all()
        else:
            videos = Video.query.all()
        videos_response = []

        for video in videos:
            videos_response.append(video.to_dict())

        return jsonify(videos_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        invalid = validate_video_request_body(request_body)
        if invalid:
            return invalid
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        return make_response(
            new_video.to_dict(), 201
        )
            

# Handles one video
@videos_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def handle_video(video_id):
    video_id = validate_id_int(video_id)
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    if request.method == "GET":
        return video.to_dict()
        
    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(
                {"message": "Invalid data"}, 400
            )
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response(video.to_dict(), 200)


# ---------------------------
# -------- RENTALS ----------
# ---------------------------

# Helper functions
def validate_rental_request_body(request_body):
    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    if "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400
    return False

def get_available_inventory(request_body):
    videos = Video.query.get(request_body["video_id"])
    
    videos_in_rentals = Rental.query.filter_by(video_id=request_body["video_id"])

    available_inventory = videos.total_inventory - videos_in_rentals.count()
    return available_inventory

# POST/Check-out a rental
@rentals_bp.route("/check-out", methods = ["POST"])
def create_rental():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_rental_request_body(request_body)

    if invalid:
        # Returns the invalid error message and status code
        return invalid
    
    due = date.today() + timedelta(days=7)
    new_rental_response = None
    
    validate_video_id = Video.query.get_or_404(request_body["video_id"])
    validate_customer_id = Customer.query.get_or_404(request_body["customer_id"])
    validate_inventory = get_available_inventory(request_body)
    if validate_inventory <= 0:
        return jsonify({"message": "Could not perform checkout"}), 400

    if validate_video_id and validate_customer_id and validate_inventory:
        new_rental = Rental(customer_id=request_body["customer_id"],
                        video_id=request_body["video_id"],
                        due_date=due

        )

        db.session.add(new_rental)
        db.session.commit()

        new_rental_response = new_rental.to_dict()

        rentals = Rental.query.filter_by(customer_id=request_body["customer_id"])
    
        videos_checked_out_count = rentals.count()
        new_rental_response["videos_checked_out_count"] = videos_checked_out_count

        after_check_out_inventory = get_available_inventory(request_body)
        
        new_rental_response["available_inventory"] = after_check_out_inventory

        videos_in_rental = Rental.query.filter_by(customer_id=request_body["customer_id"])    
        videos_checked_out_count = videos_in_rental.count()
        new_rental_response["videos_checked_out_count"] = videos_checked_out_count
        return new_rental_response

    return jsonify(new_rental_response), 200

# POST/Check-in a rental
@rentals_bp.route("/check-in", methods = ["POST"])
def update_rentals():
    request_body = request.get_json()
    if "video_id" not in request_body or "customer_id" not in request_body:
        return "Bad data", 400

    validate_video_id = Video.query.get_or_404(request_body["video_id"])
    validate_customer_id = Customer.query.get_or_404(request_body["customer_id"])
    if validate_video_id and validate_customer_id:
        rentals = Rental.query.filter_by(customer_id=request_body["customer_id"], video_id=request_body["video_id"])
        if not rentals.first():
            return make_response({"message": "No outstanding rentals for customer 1 and video 1"}, 400)

        db.session.delete(rentals.first())
        db.session.commit()
            
        videos_in_rental = Rental.query.filter_by(customer_id=request_body["customer_id"])    
        videos_checked_out_count = videos_in_rental.count()
    
        video = Video.query.get(request_body["video_id"])
        video_in_rentals = Rental.query.filter_by(video_id=request_body["video_id"])

        available_inventory = video.total_inventory - video_in_rentals.count()
        if available_inventory < 0:
            return "Could not perform checkout", 400
    
    return {
        "customer_id": request_body["customer_id"],
        "video_id": request_body["video_id"],
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory

    }, 200

# List the videos a customer currently has checked out
@customers_bp.route("/<customer_id>/rentals", methods = ["GET"])
def get_videos_by_customer(customer_id):
    customer_id = validate_id_int(customer_id)
    customer=Customer.query.get(customer_id)
    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)
    videos_in_rentals = Rental.query.filter_by(customer_id=customer_id)
    response_videos = []
    for video_in_rental in videos_in_rentals:
        video = Video.query.get(video_in_rental.video_id)
        
        response_videos.append({
        "release_date": video.release_date,
        "title": video.title,
        "due_date": video_in_rental.due_date
    })

    return jsonify(response_videos), 200


# List the customers who currently have the video checked out
@videos_bp.route("/<video_id>/rentals", methods = ["GET"])
def get_customers_by_video(video_id):
    video_id = validate_id_int(video_id)
    video=Video.query.get(video_id)
    if not video:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    customers_in_rentals = Rental.query.filter_by(video_id=video_id)
    response_customers = []
    for customer_in_rental in customers_in_rentals:
        customer = Customer.query.get(customer_in_rental.customer_id)
        
        response_customers.append({
        "due_date": customer_in_rental.due_date,
        "name": customer.name,
        "phone": customer.phone,
        "postal_code": customer.postal_code
    })
    
    return jsonify(response_customers), 200



