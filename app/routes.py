from app import db
from .helper_functions import *
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from datetime import date, timedelta
from flask import Blueprint, jsonify, request


customer_bp = Blueprint("customer", __name__, url_prefix = "/customers")
video_bp = Blueprint("video", __name__, url_prefix = "/videos")
rental_bp = Blueprint("rental", __name__, url_prefix = "/rentals")

@customer_bp.route("", methods = ["GET"])
def get_customers():
    """Returns list of dictionaries of customer info."""
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]

    return jsonify(customers_response), 200

@customer_bp.route("/<id>", methods = ["GET"])
def get_one_customer(id):
    """Returns dictionary of customer info or
    404 error if customer doesn't exist."""
    customer = valid_id(Customer, id, "customer")

    customer = customer.to_dict()

    return customer, 200

@customer_bp.route("", methods = ["POST"])
def create_customer():
    """Adds customer to database and returns new customer ID and 201 or 
    400 error if request body is missing name, phone, or postal code."""
    request_body = request.get_json()

    valid_input(request_body, Customer)
    
    new_customer = Customer(name = request_body["name"],
                            phone = request_body["phone"],
                            postal_code = request_body["postal_code"])

    add_to_database(new_customer)

    return {"id": new_customer.id}, 201

@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_one_customer(id):
    """Deletes customer and rental tied to customer if present.
        Returns ID of deleted customer. 
        Returns 404 if customer does not exist."""
    customer = valid_id(Customer, id, "customer")

    if customer.rentals:
        for rental in customer.rentals:
            delete_from_database(rental)

    delete_from_database(customer)

    return {"id": int(id)}, 200

@customer_bp.route("/<id>", methods = ["PUT"])
def update_one_customer(id):
    """Updates customer in database and 
        returns dictionary with updated customer infomation. 
        Returns 404 if customer not found or 
        400 if request body is missing name, phone, or postal code."""
    customer = valid_id(Customer, id, "customer")

    request_body = request.get_json()

    valid_input(request_body, Customer)

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    customer = customer.to_dict()
    db.session.commit()

    return customer, 200

@video_bp.route("", methods = ["GET"])
def get_videos():
    """Returns list of dictionaries of video info"""
    videos = Video.query.all()
    videos_response = [video.to_dict() for video in videos]

    return jsonify(videos_response), 200


@video_bp.route("/<id>", methods = ["GET"])
def get_one_video(id):
    """Returns dictionary of video info or
    404 error if video doesn't exist."""
    video = valid_id(Video, id, "Video")

    video = video.to_dict()

    return video, 200

@video_bp.route("", methods = ["POST"])
def create_video():
    """Adds video to database and returns new video ID and 201 or 
    400 error if request body is missing title, release_date, or total_inventory."""
    request_body = request.get_json()

    valid_input(request_body, Video)
    
    new_video = Video(title = request_body["title"],
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])

    add_to_database(new_video)

    return new_video.to_dict(), 201

@video_bp.route("/<id>", methods = ["DELETE"])
def delete_one_video(id):
    """Deletes video and rental tied to video if present.
        Returns ID of deleted video. 
        Returns 404 if video does not exist."""
    video = valid_id(Video, id, "Video")

    if video.rentals:
        for rental in video.rentals:
            delete_from_database(rental)
            
    delete_from_database(video)

    return {"id": int(id)}, 200

@video_bp.route("/<id>", methods = ["PUT"])
def update_one_video(id):
    """Updates video in database and 
        returns dictionary with updated video infomation. 
        Returns 404 if video not found or 
        400 if request body is missing title, release_date, or total_inventory."""
    video = valid_id(Video, id, "video")

    request_body = request.get_json()

    valid_input(request_body, Video)

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    video = video.to_dict()
    db.session.commit()

    return video, 200

@rental_bp.route("/<rental_action>", methods = ["POST"])
def check_video_out_or_in(rental_action): 
    """Creates new instance of rental and adds to database for checkout.
    Deletes instance of rental from database for checkin.
    Returns dictionary info of rental and 200 if successful.
    Returns 400 if missing request body incomplete or no inventory for check out.
    Returns 404 if customer or video do not exist."""
    request_body = request.get_json()
    valid_input(request_body, Rental)
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = valid_id(Customer, customer_id, "customer")
    video = valid_id(Video, video_id, "video")


    if rental_action == "check-out":
        due_date = date.today() + timedelta(days=7)

        rental = Rental(due_date = due_date,
                        customer_id = customer_id,
                        video_id = video_id)

        add_to_database(rental)
    
    if rental_action == "check-in":
        rental = Rental.query.filter(customer_id==customer_id,video_id==video_id).first()

        if not rental:
            return {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400

        delete_from_database(rental)

    available_inventory = calculate_available_inventory(rental)
    if available_inventory < 0: 
        delete_from_database(rental)
        return {"message": "Could not perform checkout"}, 400

    rental = rental.to_dict(available_inventory)
    return rental, 200

@video_bp.route("/<id>/rentals", methods = ["GET"])
def rentals_by_video(id):
    """Returns a list of dictionaries with customer's info who have a specific rental video."""
    video = valid_id(Video, id, "Video")

    rentals = video.rentals
    customer = [rental.customer.to_dict() for rental in rentals]

    return jsonify(customer), 200

@customer_bp.route("/<id>/rentals", methods = ["GET"])
def rentals_by_customer(id):
    """Returns a list of dictionaries with video info rented by a specific customer."""
    customer = valid_id(Customer, id, "Customer")

    rentals = customer.rentals
    videos = [rental.video.to_dict() for rental in rentals]
    
    return jsonify(videos), 200