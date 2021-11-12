from flask import Blueprint, request, abort, make_response
from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/<action>", methods=["POST"])
def process_rentals(action):
    request_body = request.get_json()

    try:
        video_id = valid_id(request_body["video_id"])
        customer_id = valid_id(request_body["customer_id"])

    except KeyError:
        abort(400)

    valid_video_customer(video_id, customer_id)

    if action == "check-out":
        rental = check_out(video_id, customer_id)

    elif action == "check-in":
        rental = check_in(video_id, customer_id)

    return rental.to_dict(), 200


def check_out(video_id, customer_id):

    video = Video.query.get(video_id)
    video.check_inventory()

    new_rental = Rental(customer_id=customer_id, video_id=video_id)
    db.session.add(new_rental)
    db.session.commit()
    return new_rental


def check_in(video_id, customer_id):

    rental = Rental.rental_lookup(video_id, customer_id)
    db.session.delete(rental)
    db.session.commit()

    return rental


def valid_id(id):

    try:
        id = int(id)
    except ValueError:
        abort(400)
    return id


def valid_video_customer(video_id, customer_id):

    video = Video.query.get(video_id)
    customer = Customer.query.get(customer_id)

    if not video:
        abort(
            make_response(
                {"details": f"Video with id number {video_id} was not found"}, 404
            )
        )

    elif not customer:
        abort(
            make_response(
                {"details": f"Customer with id number {customer_id} was not found"}, 404
            )
        )
