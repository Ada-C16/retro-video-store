from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.rental import Rental
from app.video_routes import valid_video
from app.customer_routes import valid_customer


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


def valid_video_customer(video_id, customer_id):

    try:
        video_id = int(video_id)
        customer_id = int(customer_id)
    except ValueError:
        abort(400)

    video = valid_video(video_id)
    customer = valid_customer(customer_id)
    return video


@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    request_body = request.get_json()

    try:
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]

        video = valid_video_customer(video_id, customer_id)

        available_inventory = video.total_inventory - len(video.rentals)
        if available_inventory <= 0:
            return {"message": "Could not perform checkout"}, 400

        new_rental = Rental(
            customer_id=customer_id,
            video_id=video_id,
        )

        db.session.add(new_rental)
        db.session.commit()

        return new_rental.to_dict(), 200

    except KeyError:
        abort(400)
