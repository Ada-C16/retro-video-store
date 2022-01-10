from types import ModuleType
from app import db
from app.customer_routes import validate_input
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
from datetime import timedelta, datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# checks out a video to a customer, and updates the data in the database
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out():
    request_data = request.get_json()
    
    validate_id(request_data)

    video = get_or_return_404(request_data["video_id"], Video)
    customer = get_or_return_404(request_data["customer_id"], Customer)

    # if the number of videos checked out == the video's total inventory, there are none left to check out
    if len(video.rentals) == video.total_inventory:
        return jsonify({"message": "Could not perform checkout"}), 400        

    new_rental = Rental(
        video_id = request_data["video_id"],
        customer_id = request_data["customer_id"]
    )
    
    db.session.add(new_rental)
    db.session.commit()

    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": len(customer.videos_rented),
        "available_inventory": video.total_inventory-len(video.rentals)
        }), 200

# checks in a video to a customer, and updates the data in the database as such
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in():
    request_data = request.get_json()
    
    validate_id(request_data)

    video_id = request_data["video_id"]
    customer_id = request_data["customer_id"]

    video = get_or_return_404(video_id, Video)
    customer = get_or_return_404(customer_id, Customer)
    
    for rental in video.rentals: # every rental of the video currently checked out
        if rental.customer_id == customer_id:
            db.session.delete(rental)
            db.session.commit()
            return jsonify({
                "customer_id": customer_id,
                "video_id": video_id,
                "videos_checked_out_count": len(customer.videos_rented),
                "available_inventory": video.total_inventory-len(video.rentals)
                }), 200
        else:
            break
    return jsonify({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}), 400

# ************************************************* ENHANCEMENTS ************************************************

# lists customer and video information about overdue rentals
@rentals_bp.route("/overdue", methods=["GET"], strict_slashes=False)
def rentals_overdue():
    rentals_overdue = []
    all_rentals = Rental.query.all()
    for this_rental in all_rentals:
        checkout_date=this_rental.due_date-timedelta(days=7)
        if (datetime.now()>(this_rental.due_date)):
            rentals_overdue.append({
                "video_id":this_rental.video_id,
                "title": this_rental.video.title,
                "customer_id": this_rental.customer_id,
                "name": this_rental.customer.name,
                "postal_code":this_rental.customer.postal_code,
                "check_out_date": checkout_date,
                "due_date_rental":this_rental.due_date
            })

    return jsonify(rentals_overdue), 200

# ********************************************** HELPER FUNCTIONS ***********************************************
def validate_id(input):
    if "customer_id" not in input:
        abort(make_response(
            {"details": "Request body must include customer_id."}, 400
        ))
        
    if "video_id" not in input:
        abort(make_response(
            {"details": "Request body must include video_id."}, 400
        ))

def get_or_return_404(id, model):
    model_object = model.query.get(id)

    if model_object is None:
        abort(make_response(
            {"details": "invalid data"}, 404
        ))

    return model_object