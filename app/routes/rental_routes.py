from flask import Blueprint, request, abort, make_response, jsonify
from app import db
from datetime import timedelta, datetime
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app.routes.video_routes import read_single_video

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def video_checkout():
    request_body=request.get_json()
    if not request_body.get("video_id") or not request_body.get("customer_id"):
        return make_response({"message":"Could not perform checkout"}, 400)

    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return make_response({"message":"Could not perform checkout"}, 404)
    elif not video:
        return make_response({"message":"Could not perform checkout"}, 404)

    total_inventory = video.total_inventory
    video_rentals = Rental.query.filter_by(video_id = video.id).count()
    available_inventory = total_inventory - video_rentals
    
    if available_inventory < 1:
        return make_response({"message": "Could not perform checkout"}),400

    else:
        available_inventory-= 1
        video_rentals+=1
        new_rental = Rental(
                customer_id=request_body["customer_id"],
                video_id=request_body["video_id"]
                )
        db.session.add(new_rental)
        db.session.commit()

        response = {"customer_id":new_rental.customer_id,
            "video_id":new_rental.video_id,
            "due_date": datetime.now() + timedelta(days=7),
            "videos_checked_out_count": video_rentals,
            "available_inventory": available_inventory}

        return make_response(response, 200)


@rentals_bp.route("/check-in", methods=["POST"])
def rental_checkin():
    request_body=request.get_json()
    if not request_body.get("video_id") or not request_body.get("customer_id"):
        return make_response({"message":"Could not perform checkin"}, 400)

    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return make_response({"message":"Could not perform checkin"}, 404)
    elif not video:
        return make_response({"message":"Could not perform checkin"}, 404)
    
    if not Rental.query.filter_by(video_id = video.id, customer_id = customer.id).first():
        return make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"},400)
        
            
    total_inventory = video.total_inventory
    video_rentals = Rental.query.filter_by(video_id = video.id).count()
    available_inventory = total_inventory - video_rentals
    videos_checked_out = Rental.query.filter_by(customer_id = customer.id).count()

    available_inventory+= 1
    video_rentals-=1
    videos_checked_out-=1

    db.session.query(Rental).filter(Rental.video_id == video.id, Rental.customer_id == customer.id).delete()
    db.session.commit()

    response = {"customer_id":customer.id,
        "video_id":video.id,
        "videos_checked_out_count": videos_checked_out,
        "available_inventory": available_inventory}

    return make_response(response, 200)