from flask import Blueprint, jsonify, make_response, request, g, abort
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app import db
from datetime import datetime, timezone, timedelta

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


@customer_bp.before_request
@video_bp.before_request
def get_model_and_label():
    """This is a function that runs before the request is processed.
    It will set g.model and g.label based on the blueprint being accessed,
    both of which are accessible globally to use in other functions.
    """
    bps = {
        "video_bp": (Video, "video"),
        "customer_bp": (Customer, "customer")
    }
    g.model, g.label = bps[request.blueprint]

# @video_bp.errorhandler(400)
# def invalid_data(errorhandler)


@customer_bp.route("", methods=["POST"])
@video_bp.route("", methods=["POST"])
def create_item():
    model = g.model
    req = request.get_json()
    new_item = model.new_from_dict(req)

    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201


@customer_bp.route("", methods=["GET"])
@video_bp.route("", methods=["GET"])
def read_items():
    model = g.model
    items = model.query.all()
    items_response = []
    for item in items:
        items_response.append(item.to_dict())
    return jsonify(items_response), 200


@customer_bp.route("/<id>", methods=["GET"])
@video_bp.route("/<id>", methods=["GET"])
def read_item(id):
    model = g.model
    item = model.get_by_id(id)
    return jsonify(item.to_dict()), 200


@customer_bp.route("/<id>", methods=["DELETE"])
@video_bp.route("/<id>", methods=["DELETE"])
def delete_item(id):
    model = g.model
    item = model.get_by_id(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(item.to_dict()), 200


@customer_bp.route("/<id>", methods=["PUT"])
@video_bp.route("/<id>", methods=["PUT"])
def update_item(id):
    model = g.model
    item = model.get_by_id(id)
    req = request.get_json()
    item = item.update(req)
    db.session.commit()
    return jsonify(item.to_dict()), 200


@rental_bp.route("/check-out", methods=["POST"])
def checkout_rental():
    req = request.get_json()

    if "video_id" not in req or "customer_id" not in req:
        abort(400)

    customer = Customer.get_by_id(req["customer_id"])
    due_date = datetime.now(timezone.utc) + timedelta(days=7)
    rental = Rental(due_date=due_date)
    rental.video = Video.get_by_id(req["video_id"])
    customer.videos.append(rental)
    db.session.commit()

    checked_out_videos = len(Rental.query.filter(
        Rental.video_id == rental.video.id).all())

    response_body = {
        "customer_id": customer.id,
        "video_id": rental.video.id,
        "due_date": rental.due_date,
        "videos_checked_out_count": checked_out_videos,
        "available_inventory": rental.video.total_inventory - checked_out_videos
    }

    return jsonify(response_body), 200


# @customer_bp.route("/<id>/rentals", methods=["GET"])
# def read_rentals(id):
#     customer = Customer.get_by_id(id)
#     rentals = []
#     for rental in customer.videos:
