from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import timedelta, date, datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# checks out a video to a customer, and updates the data in the database
    # request should:
    # create a rental for the specific video and customer
    # create a due date (7 days from current date)
    
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)

def create_check_out():
    request_body = request.get_json()
    
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    video=Video.query.get(request_body["video_id"])
    customer=Customer.query.get(request_body["customer_id"])

    # returns 404 error if missing customer, video, or no available inventory
    if customer is None or video is None:
        return jsonify({"details": "invalid data"}), 404

    # if the number of videos checked out == the video's total inventory, there are none left to check out
    if len(video.rentals) == video.total_inventory:
        return jsonify({"message": "Could not perform checkout"}), 400        

    new_rental = Rental(
        video_id = request_body["video_id"],
        customer_id = request_body["customer_id"]
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
    request_body = request.get_json()
    
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    video=Video.query.get(request_body["video_id"])
    customer=Customer.query.get(request_body["customer_id"])
    
    video_id = request_body["video_id"]
    customer_id = request_body["customer_id"]

    # returns 404 error if missing customer, video, or no available inventory
    if customer is None or video is None:
        return jsonify({"details": "invalid data"}), 404

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

#*************************************************ENHANCEMENTS************************************************
@rentals_bp.route("/overdue", methods=["GET"], strict_slashes=False)
def rentals_overdue():
    rentals_overdue = []
    all_rentals = Rental.query.all()
    for a_rental in all_rentals:
        checkout_date=a_rental.due_date -timedelta(days=7)
        if (datetime.now()>(a_rental.due_date)):
            rentals_overdue.append({
                "video_id":a_rental.video_id,
                "title": a_rental.video.title,
                "customer_id": a_rental.customer_id,
                "name": a_rental.customer.name,
                "postal_code":a_rental.customer.postal_code,
                "check_out_date": checkout_date,
                "due_date_rental":a_rental.due_date
            })

    return jsonify(rentals_overdue), 200
