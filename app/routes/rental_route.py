from flask import Blueprint, jsonify
from app import db
from app.models.rental import Rental
from .helpers import check_rental_errors

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("", methods=["GET"])
def rentals():
    rentals = Rental.query.all()
    rentals_response = [rental.to_json() for rental in rentals]
    return jsonify(rentals_response), 200

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    error_msg, video_id, customer_id = check_rental_errors()
    if error_msg is not None: 
        return error_msg
    
    # guard against trying to check out a video with no inventory 
    if Rental().get_available_inventory(video_id) <= 0:
        return { "message" : "Could not perform checkout" }, 400

    video_to_check_out = Rental(video_id=video_id, customer_id=customer_id)
    db.session.add(video_to_check_out )
    db.session.commit()

    return video_to_check_out.to_json(), 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    error_msg, video_id, customer_id = check_rental_errors()
    if error_msg is not None: 
        return error_msg

    video_to_check_in = Rental.query.filter_by(
        video_id=video_id,
        customer_id=customer_id).first()

    # guard against trying to check in a video that's not checked out
    if not video_to_check_in:
        msg = f"No outstanding rentals for customer {customer_id} and video {video_id}"
        return {"message": msg}, 400

    db.session.delete(video_to_check_in)
    db.session.commit()

    return video_to_check_in.to_json(), 200 