# Import necessary packages
from typing import NewType
from flask import Blueprint, json, jsonify, request, make_response
from flask_sqlalchemy import _make_table
from app import db
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer


# Create Blueprint for rentals

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# ----------------------------------------
# ----------- RENTALS ENDPOINTS ----------
# ----------------------------------------

# POST rentals/check-out should:
# create a rental for the specific video and customer.
# create a due date. The rental's due date is the seven days from the current date.

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()
    # Existence check
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer id"}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video id"}, 400

    # Validity check
    try:
        customer = Customer.query.get(request_body["customer_id"])
        video = Video.query.get(request_body["video_id"])
        if not customer or not video:
            return {"details": "Customer or video is None"}, 400
    except:
        return "Invalid input", 400
    

    # videos_checked_out = Rental.query.filter(Rental.video_id ==
    # request_body["video_id"], Rental.checked_out == True).count()
    
    if video.videos_checked_out_count() == video.total_inventory:
        return jsonify({
            "message": "Video not in stock"
        }), 400

    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        )

    db.session.add(new_rental)
    db.session.commit()

    response_body = {
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": video.videos_checked_out_count(),
        "available_inventory": video.available_inventory()        
    }

    return response_body, 200