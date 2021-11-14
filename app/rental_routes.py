from flask.wrappers import Response
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort
import requests

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#POST FOR CHECKOUT, CHECK-IN
@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video_to_customer():
    request_body = request.get_json()
    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify(""), 400
    video = Video.valid_int(request_body["video_id"])
    customer = Customer.valid_int(request_body["customer_id"])

    available_inventory = video.total_inventory - Rental.query.filter_by(video_id=video.id,return_date=None).count()
    if available_inventory <= 0:
        response_body = {
            "message": "Could not perform checkout"
                    }
        return jsonify(response_body), 400
    
    new_rental = Rental(customer_id=customer.id, video_id=video.id)
    db.session.add(new_rental)
    db.session.commit()

    videos_checked_out = Rental.query.filter_by(video_id=video.id,return_date=None).count()

    response_body= {"video_id":video.id,
                "customer_id": customer.id,
                "due_date": new_rental.due_date,
                "videos_checked_out_count": videos_checked_out,
                "available_inventory": video.total_inventory-videos_checked_out }
                
    return jsonify(response_body),200
    
@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video_to_customer():
    request_body = request.get_json()

    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify(""), 400
    
    video = Video.valid_int(request_body["video_id"])
    customer = Customer.valid_int(request_body["customer_id"])

    rental_record = Rental.query.filter_by(customer_id=customer.id, video_id=video.id, return_date=None).first()

    if not rental_record:
        response_body = {
            "message": f"No outstanding rentals for customer {customer.id} and video {video.id}"
            }
        return jsonify(response_body), 400

    rental_record.return_date = date.today()

    db.session.commit()

    videos_checked_out = Rental.query.filter_by(video_id=video.id,return_date=None).count()

    response_body= {"video_id":video.id,
                "customer_id": customer.id,
                "videos_checked_out_count": videos_checked_out,
                "available_inventory": video.total_inventory-videos_checked_out }
                
    return jsonify(response_body), 200


# WAVE 03 CUSTOM ENDPOINT

@rentals_bp.route("/overdue", methods=["GET"])
def read_all_customers_with_overdue_rentals():

    overdue_rentals = Rental.query.filter(Rental.due_date<date.today(), Rental.return_date==None).all()

    list_of_customers = []

    for rental in overdue_rentals:
        video = Video.query.get(rental.video_id)
        customer = Video.query.get(rental.customer_id)

        customer_data = {
            "video_id": video.id,
            "title": video.title,
            "customer_id": customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": rental.checkout_date,
            "due_date": rental.due_date
        }

        list_of_customers.append(customer_data)

    return jsonify(list_of_customers), 200


#GET AT THE CUSTOMERS_ID_RENTALS, GET VIDEOS_ID_RENTALS
