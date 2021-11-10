from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response,request, abort
from dotenv import load_dotenv
import os
from datetime import date, timedelta 
from flask import Flask


load_dotenv()
rental_bp = Blueprint("rental", __name__,url_prefix="/rentals")

#Helper function
def valid_int(number):
    try:
        return int(number)     
    except:
        abort(make_response({"error": f"{number} must be an int"}, 400))

@rental_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify({"message":f"Rental 1 was not found"}), 404

   
#Helper function
# def get_customer_from_id(customer_id):
#     customer_id = valid_int(customer_id)
#     return Customer.query.get_or_404(customer_id)

@rental_bp.route("/check_out", methods="POST")
def create_customer_video():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    if "videos_checked_out_count" not in request_body:
        videos_checked_out_count = 1
    due_date = date.today() + timedelta(days=7)
    this_video = Video.query.get(video_id)
    total_inventory = this_video.total_inventory

    new_rental = Rental(video_id=video_id, customer_id=customer_id, videos_checked_out_count=videos_checked_out_count)
    
    db.session.add(new_rental)
    db.session.commit()

    return {
  "customer_id": new_rental.customer_id,
  "video_id": new_rental.video_id,
  "due_date": due_date,
  "videos_checked_out_count": videos_checked_out_count,
  "available_inventory":total_inventory - videos_checked_out_count
}