from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods = ["POST"])
def rental_check_out():
    rental_request = request.get_json()

    if "customer_id" not in rental_request or "video_id" not in rental_request:
        return jsonify(details="Request body must include customer id and video id"), 400

    customer_id = rental_request["customer_id"]
    video_id = rental_request["video_id"]

    try: 
        video_id = int(video_id)
        customer_id = int(customer_id)
    except:
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    if customer is None or video is None:
        return jsonify(None), 404

    num_currently_checked_out = Rental.query.filter_by(video_id=video.id, checked_out=True).count()
    available_inventory = video.total_inventory - num_currently_checked_out

    if available_inventory == 0:
        return jsonify(message="Could not perform checkout"), 400

    new_rental_check_out= Rental(
        customer_id=customer.id,
        video_id=video.id,
        due_date=(datetime.now() + timedelta(days=7)),
        checked_out=True
    )

    db.session.add(new_rental_check_out)
    db.session.commit()

    available_inventory -= 1

    videos_customer_checked_out = Rental.query.filter_by(customer_id=customer.id, checked_out=True).count()
    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": new_rental_check_out.due_date,
        "videos_checked_out_count": videos_customer_checked_out,
        "available_inventory": available_inventory
    }, 200


@rentals_bp.route("/check-in", methods = ["POST"])
def rental_check_in():
    rental_request = request.get_json()

    if "customer_id" not in rental_request or "video_id" not in rental_request:
        return jsonify(details="Request body must include customer id and video id"), 400

    customer_id = rental_request["customer_id"]
    video_id = rental_request["video_id"]

    try: 
        video_id = int(video_id)
        customer_id = int(customer_id)
    except:
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None or video is None:
        return jsonify(None), 404
    
    rental = Rental.query.filter_by(customer_id=customer.id, video_id=video.id, checked_out=True).first()
    if rental is None:
        return jsonify(message=f"No outstanding rentals for customer {customer.id} and video {video.id}"), 400

    rental.checked_out = False
    db.session.commit()

    num_currently_checked_out = Rental.query.filter_by(video_id=video.id, checked_out=True).count()
    available_inventory = video.total_inventory - num_currently_checked_out
    videos_customer_checked_out = Rental.query.filter_by(customer_id=customer.id, checked_out=True).count()
    
    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": videos_customer_checked_out,
        "available_inventory": available_inventory
    }, 200








