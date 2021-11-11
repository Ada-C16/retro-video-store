from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def rental_check_out():
    
    request_body = request.get_json()

    #CHECK FOR VALID INPUT TYPE HERE
    #need to ensure that each data type is correct

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    #add here: check for inventory, return "message": "Could not perform checkout", 400

    #name variables for clarity later in code
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    #check to make sure customer and video exist
    if video is None or customer is None:
        return jsonify(None), 404

    new_rental = Rental(customer_id=customer.id,\
    video_id=video.id, due_date=(datetime.now() + timedelta(12)))

    db.session.add(new_rental)
    db.session.commit()

    #removed helper function bc you can sort by multiple variables, no need for looping
    
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

    #isdigit() evaluates to True if string is actually numbers, so this line checks to make sure 
    #both ids are actually numbers and if not it returns 400

    # if request_body["customer_id"].isdigit() and request_body["customer_id"].isdigit():
    #     pass
    # else:
    #     return jsonify(None), 400

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    #check to make sure customer and video exist
    if video is None or customer is None:
        return jsonify(None), 404

    rental = Rental.query.filter_by(customer_id=customer.id, video_id=video.id, checked_in=False).first()
    
    if rental is None:
        response_body = {"message": "No outstanding rentals for customer 1 and video 1"} 
        return jsonify(response_body), 400

    rental.checked_in = True

    db.session.commit()

    #removed helper function bc you can sort by multiple variables, no need for looping
    
    num_videos_checked_out =  Rental.query.filter_by(video_id=video.id, checked_in=False).count() #.count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(customer_id=customer.id, checked_in=False).count()

    response_body = {
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }

    return response_body, 200