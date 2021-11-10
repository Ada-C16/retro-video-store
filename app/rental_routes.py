from flask.wrappers import Response
from app import db
from app.models.video import Video
from app.video_routes import get_video_from_id, valid_int
from app.models.customer import Customer
from app.customer_routes import get_customer_from_id, valid_int
from app.models.rental import Rental
from datetime import date
from flask import Blueprint, jsonify, make_response, request, abort
import requests

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#POST FOR CHECKOUT, CHECK-IN
@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video_to_customer():
    request_body = request.get_json()
    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify(""), 400
    video = get_video_from_id(request_body["video_id"])
    customer = get_customer_from_id(request_body["customer_id"])

    available_inventory = video.total_inventory - Rental.query.filter_by(video_id=video.id,return_date=None).count()
    if available_inventory <= 0:
        response_body = {
            "message": "Could not perform checkout"
                    }
        return jsonify(response_body), 400
    
    new_rental = Rental(customer_id=customer.id, video_id=video.id)
    db.session.add(new_rental)
    db.session.commit()

    videos_checked_out = Rental.query.filter_by(video_id=video.id,return_date=None).count()

    response_body= {"video_id":video.id,
                "customer_id": customer.id,
                "due_date": new_rental.due_date,
                "videos_checked_out_count": videos_checked_out,
                "available_inventory": video.total_inventory-videos_checked_out }
                
    return jsonify(response_body),200
    
@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video_to_customer():
    pass
#GET AT THE CUSTOMERS_ID_RENTALS, GET VIDEOS_ID_RENTALS
