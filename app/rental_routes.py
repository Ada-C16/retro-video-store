from app import db
from app.customer_routes import customers_bp
from app.video_routes import video_bp
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def rentals_checkout():
    #{"c_id": [1], "v_id": [4]}
    request_body = request.get_json() 

    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify(), 400

    customer = Customer.query.get(request_body["customer_id"])
    if customer is None:
        return jsonify(), 404

    video = Video.query.get(request_body["video_id"])
    if video is None:
        return jsonify(), 404

    if video.total_inventory == 0:
        return jsonify({"message": "Could not perform checkout"}), 400

    # Instantiate a new instance for rental
    new_rental = Rental(
        video_id=video.video_id,
        customer_id=customer.customer_id
    )  
    
    # add rental instance to database
    db.session.add(new_rental)
    # commit to database
    db.session.commit()
    
    # return the response body and status code
    return jsonify({
        "video_id": new_rental.video_id,
        "customer_id": new_rental.customer_id,
        "videos_checked_out_count": len(customer.videos),
        "available_inventory": video.total_inventory - len(video.customers)
    }), 200



@rentals_bp.route("/check-in", methods=["POST"])
def rentals_checkin():
    pass

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_read(customer_id):
    """ List the videos a customer currently has checked out """
    pass

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def video_read(video_id):
    """ List the customers who currently have the video checked out """
    # videos_list = []
    # for video in self.videos:
    #     videos_list(video.rental_id)
    pass