from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import *
from flask import Blueprint, request, make_response
import datetime as dt
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
        return make_response("invalid input", 400)
    if customer is None or video is None:
        return make_response("", 404)
    if count_a_videos_inventory(video.id, video.total_inventory) == 0:
        return make_response({"message":"Could not perform checkout"}, 400)

    new_rental = Rental(
        customer = customer.id,
        video = video.id,
        due_date = dt.datetime.now() + dt.timedelta(days = 7),
        videos_checked_out_count = len(query_customers_videos(customer.id)) + 1,
        available_inventory = count_a_videos_inventory(video.id, video.total_inventory) - 1,
        checked_in = False
    )

    db.session.add(new_rental)
    db.session.commit()    
    
    return make_response(new_rental.to_json(), 200)


@rental_bp.route("/check-in", methods = ["POST"])
def check_in_rental():
    pass



