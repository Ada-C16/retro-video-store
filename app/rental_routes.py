from app import db
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video


rentals_bp = Blueprint("rentals",__name__, url_prefix="/rentals")
@rentals_bp.route("/<register>",methods=["GET","POST"])
def handle_rental(register):
    if register == "check-in":
        pass
    elif register == "check-out":
        request_body = request.get_json()
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)

        rental = Rental(
            customer_id=customer.customer_id,
            video_id=video.video_id
        )
        customer.rentals.append(rental)
        video.rentals.append(rental)
        
        customer.videos_checked_out_count += 1
        video.available_inventory -= 1
        db.session.commit()
        return make_response(jsonify(create_checkout_dict(video, customer)), 200) 

def create_checkout_dict(video, customer):
    result = {"video_id" : video.video_id,
    "customer_id" : customer.customer_id,
    "videos_checked_out_count" : customer.videos_checked_out_count,
    "available_inventory" : video.available_inventory}
    return result
    