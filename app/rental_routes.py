from flask import Blueprint, request, abort
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
    valid_customer(customer_id)
    return video


@rentals_bp.route("/<action>", methods=["POST"])
def check_out(action):
    request_body = request.get_json()

    try:
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]

        video = valid_video_customer(video_id, customer_id)
        if action == "check-out":
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

        elif action == "check-in":
            rental = Rental.query.filter(
                video_id == video_id, customer_id == customer_id
            ).first()
            if not rental:
                return {
                    "message": f"No outstanding rentals for customer {customer_id} and video {video_id}"
                }, 400
            db.session.delete(rental)
            db.session.commit()

            return rental.to_dict(), 200

    except KeyError:
        abort(400)
