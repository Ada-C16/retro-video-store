from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, abort
from datetime import datetime, timedelta
from app.routes.video_routes import check_for_valid_input

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def validate_input(request_body):
    '''ensure all input from request body is a correct 
    and valid data type, abort and return 400 error 
    message if the data is not valid'''
    for key, value in request_body.items():
        if type(value) is not int:
            error_message = jsonify({"Invalid Input": f"The {key} value must be an integer."})

            return abort(400, error_message)

@rentals_bp.route("/check-out", methods=["POST"])
def rental_check_out():
    
    request_body = request.get_json()

    list_of_attributes = ["customer_id", "video_id"]

    check_for_valid_input(request_body, list_of_attributes)

    validate_input(request_body)

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video is None or customer is None:
        return jsonify(None), 404
        
    num_current_checked_out =  Rental.query.filter_by(video_id=video.id, checked_in=False).count() #.count() returns length
    current_available_inventory = video.total_inventory - num_current_checked_out

    if current_available_inventory == 0:
        return jsonify({ 
                "message": "Could not perform checkout"
                }), 400

    new_rental = Rental(customer_id=customer.id,\
    video_id=video.id, due_date=(datetime.now() + timedelta(days=7)))

    db.session.add(new_rental)
    db.session.commit()
    
    num_videos_checked_out =  Rental.query.filter_by(video_id=video.id, checked_in=False).count() #.count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(customer_id=customer.id, checked_in=False).count()

    response_body = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }
    return response_body, 200

@rentals_bp.route("/check-in", methods=["POST"])
def rental_check_in():
    
    request_body = request.get_json()

    list_of_attributes = ["customer_id", "video_id"]

    check_for_valid_input(request_body, list_of_attributes)

    validate_input(request_body)

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    if video is None or customer is None:
        return jsonify(None), 404

    rental = Rental.query.filter_by(customer_id=customer.id, video_id=video.id, checked_in=False).first()
    
    if rental is None:
        response_body = {"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"} 
        return jsonify(response_body), 400

    rental.checked_in = True

    db.session.commit()
    
    num_videos_checked_out =  Rental.query.filter_by(video_id=video.id, checked_in=False).count() 
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(customer_id=customer.id, checked_in=False).count()

    response_body = {
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }

    return response_body, 200