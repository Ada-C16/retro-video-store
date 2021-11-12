from flask import Blueprint, request, abort, make_response
from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app.validate import Validate


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/<action>", methods=["POST"])
def process_rentals(action):
    request_body = request.get_json()

    try:
        video_id = Validate.valid_id(request_body["video_id"])
        customer_id = Validate.valid_id(request_body["customer_id"])

    except KeyError:
        abort(400)

    Validate.valid_video(video_id, action=True)
    Validate.valid_customer(customer_id, action=True)

    if action == "check-out":
        rental = Rental.check_out(video_id, customer_id)

    elif action == "check-in":
        rental = Rental.check_in(video_id, customer_id)

    return rental.rental_dict(), 200
