import re
from app import customer_routes, db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from datetime import date, datetime, timedelta
from flask import Blueprint, jsonify, request


rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rental_bp.route("/check-out", methods=["POST"])
def rental_check_out():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return jsonify(None), 400
    if "video_id" not in request_body:
        return jsonify("Could not perform checkout"), 400
    
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    if hasattr(video, 'rentals') is False:
        return jsonify(None), 404
    if hasattr(customer, 'rentals') is False:
        return jsonify(None), 404
    count_of_rentals = len(video.rentals)

    video_avialable_inventory = video.total_inventory - count_of_rentals

    if video_avialable_inventory==0:
        response_body={
            "message":"Could not perform checkout"
        }
        return jsonify(response_body), 400

    today = datetime.today()
    due_date = today + timedelta(days=7)

    new_rental = Rental(customer_id=customer.id, video_id=video.id, due_date=due_date, checked_out=True)

    
    db.session.add(new_rental)
    db.session.commit()

    video_avialable_inventory -= 1
    videos_customer_checked_out = Rental.query.filter_by(customer_id=customer.id, checked_out=True).count()

    response_body = {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": due_date,
        "videos_checked_out_count": videos_customer_checked_out,
        "available_inventory": video_avialable_inventory,
    }
    
    return jsonify(response_body), 200


@rental_bp.route("/check-in", methods=["POST"])
def rental_check_in():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return jsonify("Request body must include customer id and video id"), 400
    if "video_id" not in request_body:
        return jsonify("Request body must include customer id and video id"), 400

    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    rental = Rental.query.filter_by(customer_id=customer.id, video_id=video.id, checked_out=True)
    
    if rental.customer_id is False:
        return jsonify(None), 404
    if rental.video_id is False:
        return jsonify(None), 404
    if customer is None or video is None:
        return jsonify(None), 404
    if rental is None:
        return jsonify(message="No outstanding rentals for customer 1 and video 1"), 400
    if hasattr(video, 'rentals') is False:
        return jsonify(None), 404
    if hasattr(customer, 'rentals') is False:
        return jsonify(None), 404
    
    
    count_of_rentals = len(video.rentals)

    db.session.delete(rental)
    db.session.commit()

    videos_customer_checked_out = Rental.query.filter_by(customer_id=customer.id, checked_out=True).count()
    video_avialable_inventory = video.total_inventory - count_of_rentals


    response_body = {
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": videos_customer_checked_out,
        "available_inventory": video_avialable_inventory+1,
    }

    return jsonify(response_body), 200
