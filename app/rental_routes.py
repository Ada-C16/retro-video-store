from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from flask import Blueprint, jsonify, request



rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"])
def handle_rental_checkout():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    # print(video)
    available_inventory = Rental.calc_available_inventory(video_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    elif video is None:
        return ({"message": f"Video {video_id} was not found"}, 404)
    elif available_inventory == 0:
        return ("Could not perform checkout", 400) 
    else:
        new_rental = Rental.from_json(request_body)
        db.session.add(new_rental)
        db.session.commit()
        return jsonify(new_rental.to_json()), 200

@rentals_bp.route("/check-in", methods=["POST"])
def handle_rental_checkin():
    request_body = request.get_json()
    try:
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
    except KeyError:
        if "customer_id" not in request_body:
            return {"details": "Request body must include customer_id."}, 400
        elif "video_id" not in request_body:
            return {"details": "Request body must include video_id."}, 400
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    elif video is None:
        return ({"message": f"Video {video_id} was not found"}, 404)
    rental = Rental.query.get(customer_id, video_id)
    if rental is None:
        return ({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400) 
    else:
        db.session.delete(rental)
        db.session.commit()
        video = Video.query.get(video_id)
        return {
            "customer_id": customer_id,
            "video_id": video_id,
            "videos_checked_out_count": Rental.calc_videos_checked_out(customer_id),
            # "available_inventory": Rental.calc_available_inventory(video_id)
            "videos_checked_out_count": calc_available_inventory(video_id)
        }, 200

def calc_available_inventory(video_id):
    total_inventory = Video.query.get(video_id).total_inventory
    checked_out = Rental.query.filter(Rental.video_id == video_id).count()
    available_inventory = total_inventory - checked_out
    return available_inventory