from flask import Blueprint, request, make_response, abort, jsonify
from app.models.rental import Rental
from .helper_functions import *
from app import db
from datetime import datetime, timedelta

# Blueprint
rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

@rentals_bp.route('/check-out', methods=['POST'], strict_slashes=False)
def check_out_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    video = get_video_from_id(request_body['video_id'])
    # check if video is available
    total_inventory = int(video.total_inventory)
    total_checked_out = len(Rental.query.filter_by(video_id=video.id, checked_in=False).all())
    available_inv = total_inventory - total_checked_out
    if available_inv < 1:
        abort(make_response({'message': 'Could not perform checkout'}, 400))
    # create new rental
    get_customer_data_with_id(request_body['customer_id'])
    new_rental = Rental(
        customer_id = request_body['customer_id'],
        video_id = request_body['video_id'],
        )
    db.session.add(new_rental)
    db.session.commit()
    return make_response(new_rental.to_dict(), 200)

@rentals_bp.route('/check-in', methods=['POST'], strict_slashes=False)
def check_in_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    # check if video and customer IDs are valid
    get_video_from_id(request_body['video_id'])
    get_customer_data_with_id(request_body['customer_id'])
    # find rental record
    rental_record = Rental.query.filter_by(
            customer_id=request_body['customer_id'], 
            video_id=request_body['video_id'], 
            checked_in=False
            ).first()
    if not rental_record:
        return make_response(
            {"message": 
            f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}, 400)
    rental_record.checked_in = True
    db.session.commit()
    return make_response(rental_record.to_dict(), 200)


# OPTIONAL ROUTES

@rentals_bp.route('/overdue', methods=['GET'], strict_slashes=True)
def get_overdue_videos():
    overdue_movie_records = Rental.query.filter(Rental.checked_in==False, Rental.due_date<datetime.now()).all()
    response = []
    for record in overdue_movie_records:
        video = get_video_from_id(record.video_id)
        customer = get_customer_data_with_id(record.customer_id)
        response.append({
            "video_id": record.video_id,
            "title": video.title,
            "customer_id": record.customer_id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": record.due_date - timedelta(days=7),
            "due_date": record.due_date,
            
        })
    return make_response(jsonify(response), 200)