from app import db
from customer_routes import customers_bp
from video_routes import video_bp
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def rentals_checkout():
    request_body = request.get_sjson()
    """
    get request body from client
    check to make sure required attributes are in request body
    Instantiate a new instance for rental
    ?customer.videos or video.customers?
    add rental instance to database
    commit to database
    return the response body and status code
    
    """

@rentals_bp.route("/check-in", methods=["POST"])
def rentals_checkin():
    pass

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_read():
    pass

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def video_read():
    pass