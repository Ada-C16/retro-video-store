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
    if video.total_inventory == 0:
        response_body = {"message": "Could not perform checkout"}
        return jsonify(response_body), 400
    new_inventory_total = video.total_inventory - 1
    video.total_inventory = new_inventory_total

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify(None), 404
    videos_checked_out = customer.videos_checked_out + 1
    customer.videos_checked_out = videos_checked_out

    new_rental = Rental(
        video_id=request_body["video_id"],
        customer_id=request_body["customer_id"]
    )

    db.session.add(new_rental)
    db.session.commit()
    response_body = new_rental.rental_dict()
    return jsonify(response_body), 200
