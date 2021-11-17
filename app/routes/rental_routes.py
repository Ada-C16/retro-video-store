from flask import Blueprint, request, make_response, abort, jsonify
from app.models.rental import Rental
from .helper_functions import *
from app import db
from datetime import datetime, timedelta

# Blueprint
rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

#this route needs to connect rentals with videos/customers
@rentals_bp.route('/check-out', methods=['POST'], strict_slashes=False)
def check_out_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    video = get_video_from_id(request_body['video_id'])
    available_inventory = video.total_inventory - len(video.rentals)
    if available_inventory < 1:
        abort(make_response({'message': 'Could not perform checkout'}, 400))
    # check if customer id is valid
    get_customer_data_with_id(request_body['customer_id'])
    new_rental = Rental(
        customer_id = request_body['customer_id'],
        video_id = request_body['video_id'],
        )
    try:
        db.session.add(new_rental)
        db.session.commit()
    except:
        db.session.rollback()
        return make_response({"error":"Video could not be checked out"}, 400)
    return make_response(new_rental.to_dict(), 200)

@rentals_bp.route('/check-in', methods=['POST'], strict_slashes=False)
def check_in_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        return make_response({'error': 'customer_id and video_id are required'}, 400)
    #check if video and customer IDs are valid
    video = get_video_from_id(request_body['video_id'])
    customer = get_customer_data_with_id(request_body['customer_id'])
    #find rental record
    rental_record = Rental.query.filter(video==video, customer==customer).first()
    if not rental_record:
        return make_response(
            {"message": 
            f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}, 400)
    try:
        db.session.delete(rental_record)
        db.session.commit()
    except:
        db.session.rollback()
        return make_response({'error':'Video was not successfully returned'}, 400)
    return make_response(rental_record.to_dict(), 200)


# OPTIONAL ROUTES

@rentals_bp.route('/overdue', methods=['GET'], strict_slashes=True)
def get_overdue_videos():
    overdue_movie_records = Rental.query.filter(Rental.due_date<datetime.now()).all()
    response = []
    for record in overdue_movie_records:
        response.append({
            "video_id": record.video_id,
            "title": record.video.title,
            "customer_id": record.customer_id,
            "name": record.customer.name,
            "postal_code": record.customer.postal_code,
            "checkout_date": record.due_date - timedelta(days=7),
            "due_date": record.due_date,           
        })
    return make_response(jsonify(response), 200)