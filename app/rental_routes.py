from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        response_body = {"details": "Request body must include customer_id."}
        return jsonify(response_body), 400
    elif "video_id" not in request_body:
        response_body = {"details": "Request body must include video_id."}
        return jsonify(response_body), 400

    video_id = request_body["video_id"]
    customer_id = request_body["customer_id"]
    video = Video.query.get(video_id)
    if not video:
        return jsonify(None), 404
    video_inventory = video.total_inventory - len(video.rentals)
    if video_inventory == 0:
        response_body = {"message": "Could not perform checkout"}
        return jsonify(response_body), 400

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify(None), 404

    new_rental = Rental(
        video_id=request_body["video_id"],
        customer_id=request_body["customer_id"]
    )

    db.session.add(new_rental)
    customer.videos_checked_out = len(customer.rentals)
    db.session.commit()
    response_body = new_rental.rental_dict()
    return jsonify(response_body), 200


@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        response_body = {"details": "Request body must include customer_id."}
        return jsonify(response_body), 400
    elif "video_id" not in request_body:
        response_body = {"details": "Request body must include video_id."}
        return jsonify(response_body), 400

    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)

    if not (video and customer):
        response_body = {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}
        return jsonify(response_body), 404

    if customer.videos_checked_out == 0:
        response_body = {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}
        return jsonify(response_body), 400

    Rental.query.filter_by(customer_id=customer_id, video_id=video_id).delete()

    customer.videos_checked_out = len(customer.rentals)
    response_body = Rental.checkin_dict(customer, video)
    return jsonify(response_body), 200
