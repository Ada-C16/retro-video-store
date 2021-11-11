from flask import Blueprint, abort, jsonify, make_response, request

from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video

rentals_bp = Blueprint("rentals",__name__, url_prefix="/rentals")

@rentals_bp.route("/<register>",methods=["GET","POST"])
def handle_rental(register):
    request_body = request.get_json()
    cust_id, vid_id = validates_request_body(request_body)
    customer = Customer.query.get(cust_id)
    video = Video.query.get(vid_id)
    if register == "check-in":
        rental = db.session.query(Rental).filter(Rental.customer_id == cust_id, Rental.video_id == vid_id).first()
        if not rental:
            return make_response({"message": f"No outstanding rentals for customer {cust_id} and video {vid_id}"}, 400)
            

        db.session.delete(rental)
        customer.videos_checked_out_count -= 1
        db.session.commit()
        return make_response(jsonify(create_checkout_dict(video,customer)),200)

    elif register == "check-out":
        rental = Rental(
            customer_id=customer.customer_id,
            video_id=video.video_id
        )
        if video.gets_available_inventory() == 0:
            return make_response({"message":"Could not perform checkout"}, 400)

        customer.rentals.append(rental)
        video.rentals.append(rental)
        
        customer.videos_checked_out_count += 1
            
        db.session.commit()
        return make_response(jsonify(create_checkout_dict(video, customer)), 200) 

def create_checkout_dict(video, customer):
    result = {"video_id" : video.video_id,
    "customer_id" : customer.customer_id,
    "videos_checked_out_count" : customer.videos_checked_out_count,
    "available_inventory" : video.gets_available_inventory()}
    return result

def validates_request_body(request_body):
    if "customer_id" not in request_body or "video_id" not in request_body:
        abort(make_response(jsonify({"error" : "Missing customer_id or video_id"}),400))
    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)
    if not customer:
        abort(make_response("Customer not found", 404))
        
    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    if not video:
        abort(make_response("Video not found", 404))

    return customer_id, video_id  

def deletes_rentals(id, customer_id=False):
    if customer_id == True:
        rentals = db.session.query(Rental).filter(Rental.customer_id == id).all()
        for rental in rentals:
            db.session.delete(rental)
        db.session.commit()
    else:
        rentals = db.session.query(Rental).filter(Rental.video_id == id).all()
        for rental in rentals:
            db.session.delete(rental)
        db.session.commit()
