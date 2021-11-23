from app import db
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint,  request, make_response, jsonify
from datetime import datetime, timedelta, timezone
from app.routes.helper_functions import * 
rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')



'''
handling request, 
is it valid?, 
getting filtered data, 
checking out, 
returning data
'''
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    request_body = request.get_json()
    validate_request("checkout", request_body)
    customer, video = get_customer_and_video_id(request_body)

    videos_checked_out_by_customer_count = Rental.query.filter_by(customer_id=customer.id).count()
    videos_id_checked_out_count = Rental.query.filter_by(video_id=video.id).count()
    available_inventory = video.total_inventory - videos_id_checked_out_count

    if not available_inventory:   
        return make_response({"message": f"Could not perform checkout"},400)
    
    videos_checked_out_by_customer_count += 1
    available_inventory -= 1
    checked_out_date =datetime.utcnow() 
    due_date = checked_out_date + timedelta(days=7)

    new_rental = Rental(video_id=video.id,
                        customer_id=customer.id,
                        due_date=due_date, 
                        available_inventory=available_inventory,
                        videos_checked_out_count=videos_checked_out_by_customer_count,
                        checkout_date= checked_out_date)

    db.session.add(new_rental)
    db.session.commit() 
    response_body = new_rental.to_dict()
    return make_response(response_body, 200)


# Post check-in
'''
* handling request,
* is it valid?, 
* getting filtered data, 
* handling test_checkin_video_not_checked_out, 
* checking in rental, returning data
'''
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():

    request_body = request.get_json()

    validate_request("checkin", request_body)
    customer, video = get_customer_and_video_id(request_body)
    rentals = Rental.query.filter_by(video_id=video.id, customer_id=customer.id).one_or_none()

    if rentals == None:
        return make_response({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400)

    if not rentals.checked_in:
        rentals.due_date = None,
        rentals.available_inventory =  rentals.available_inventory + 1
        rentals.videos_checked_out_count=  rentals.videos_checked_out_count - 1
        rentals.checked_in =datetime.utcnow()

        db.session.commit() 

    response_body = rentals.to_dict()
    return make_response(response_body, 200)

@rentals_bp.route("/overdue", methods=["GET"], strict_slashes=False)
def get_overdue_videos():
    now = datetime.now(timezone.utc)
    rentals_overdue = Rental.query.filter(Rental.due_date < now).all()
    response_body = []

    for rental in rentals_overdue:
        customer = get_customer_from_id(rental.customer_id)
        video = get_video_by_id(rental.video_id)

        response_body.append(
            {"customer_id": rental.customer_id,
            "video_id": rental.video_id,
            "Video Title": video.title,
            "Costumer name": customer.name,
            "postal_code": customer.postal_code,
            "due_date":rental.due_date,
            "checkout_date":rental.checkout_date
            }
        )

    return make_response(jsonify(response_body), 200)