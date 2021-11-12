from flask import Blueprint, jsonify
from app import db
from app.models.rental import Rental
from .helpers import id_is_valid, request_has_all_required_categories

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("", methods=["GET"])
def rentals():
    rentals = Rental.query.all()
    rentals_response = [rental.to_json() for rental in rentals]
    return jsonify(rentals_response), 200

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_data, error_msg = request_has_all_required_categories("rental")
    if error_msg is not None:
        return error_msg 

    video_id = request_data["video_id"]
    _, error_msg = id_is_valid(str(video_id), "video")
    if error_msg is not None:
        return error_msg 
    
    customer_id = request_data["customer_id"]
    _, error_msg = id_is_valid(str(customer_id), "customer")
    if error_msg is not None:
        return error_msg 
    
    # guard against trying to rent out something with no inventory 
    if Rental().get_available_inventory(video_id) <= 0:
        return { "message" : "Could not perform checkout" }, 400

    new_rental = Rental(video_id=video_id, customer_id=customer_id)
    db.session.add(new_rental)
    db.session.commit()

    return new_rental.to_json(), 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_data, error_msg = request_has_all_required_categories("rental")
    if error_msg is not None:
        return error_msg 

    video_id = request_data["video_id"]
    _, error_msg = id_is_valid(str(video_id), "video")
    if error_msg is not None:
        return error_msg 
    
    customer_id = request_data["customer_id"]
    _, error_msg = id_is_valid(str(customer_id), "customer")
    if error_msg is not None:
        return error_msg 

    find_rental = "video_not_checked_out"
    rentals = Rental.query.all() # figure out something like filter_by(video_id=video_id)
    for rental in rentals:
        if rental.video_id == video_id and rental.customer_id == customer_id: 
            find_rental = rental 

    if find_rental == "video_not_checked_out":
        msg = f"No outstanding rentals for customer {customer_id} and video {video_id}"
        return {"message": msg}, 400

    db.session.delete(find_rental)
    db.session.commit()

    return find_rental.to_json(), 200 