from flask import Blueprint, jsonify, make_response, request, abort
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from app.routes.customer_routes import get_customer_from_id
from app.routes.video_routes import is_parameter_found
from app import db
from datetime import datetime, timezone, timedelta
import requests
import os

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rental_bp.route("/check-out", methods=["POST"])
def checkout_rental():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        abort(400, "Request body must include a customer_id and video_id")

    customer = get_customer_from_id(request_body["customer_id"])
    video = is_parameter_found(Video, request_body["video_id"])

    # if total inventory is empty (unsure if it's testing against 0 or None, couldn't tell on test)
    if video.total_inventory - len(video.rentals) == 0:
        abort(make_response({"message":"Could not perform checkout"}, 400))


    new_rental = Rental(customer_id=customer.id, video_id=video.id)
    # new_rental.checkout_date = datetime.now(timezone.utc)
    # days = datetime.timedelta(days=7)
    # due_date = new_rental.checkout_date + days

    db.session.add(new_rental)
    db.session.commit()
    
    # customer_videos = db.session.query(video).filter(Rental.customer_id==customer.id).all()
    # videos_checked_out_count = len(customer_videos)

    # how many videos are checked out
    
    # unavailable_videos = db.session.query(video).filter(Rental.video_id==video.id).all()
    # videos_checked_out_count = len(unavailable_videos)
    videos_checked_out_count = video.rentals
    available_inventory = video.total_inventory - len(video.rentals)

    return jsonify(new_rental.to_dict(videos_checked_out_count,available_inventory)), 200

