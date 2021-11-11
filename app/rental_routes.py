from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import *
from flask import Blueprint, request, make_response
import os 

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

'''
@rental_bp.route("", methods = ["GET"])
def get_rentals():    
    pass
'''

@rental_bp.route("/check-out", methods = ["POST"])
def check_out_rental():
    request_body = request.get_json()
    try:
        customer = Customer.query.get(request_body["customer_id"])
        video = Video.query.get(request_body["video_id"])
    except:
        return make_response("invalid input", 404)
    if customer or video is None:
        return make_response("", 404)
    if Rental.count_a_videos_inventory(video.id) == 0:
        return make_response("", 400)
    return make_response(Rental.check_out_json(customer.id, video.id), 200)

@rental_bp.route("/check-in", methods = ["POST"])
def check_in_rental():
    pass