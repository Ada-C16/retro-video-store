from flask import Blueprint, request, make_response, abort, jsonify
from app.models.rental import Rental
from app.models.video import Video
from app.routes.video_routes import get_video_from_id
from app.routes.customer_routes import get_customer_data_with_id
from app.models.customer import Customer
from app import db
from datetime import datetime, timedelta

#helper functions
# def validate_id(id, id_type):
#     try:
#         int(id)
#     except:
#         abort(make_response({"error": f"{id_type} must be an int"}, 400))

# def get_video_from_id(id):
#     validate_id(id, 'video id')
#     selected_video = Video.query.get(id)
#     if not selected_video:
#         abort(make_response({'message': f'Video {id} was not found'}, 404))
#     return selected_video

# def get_customer_data_with_id(customer_id):
#     validate_id(customer_id, "id")
#     customer = Customer.query.get(customer_id)

#     if customer is None:
#         abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

#     return customer

# Blueprint
rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

@rentals_bp.route('/check-out', methods=['POST'], strict_slashes=False)
def check_out_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    video = get_video_from_id(request_body['video_id'])
    # check if inventory is non-zero
    total_inventory = int(video.total_inventory)
    total_checked_out = len(Rental.query.filter_by(video_id=video.id, checked_in=False).all())
    available_inv = total_inventory - total_checked_out
    if available_inv < 1:
        abort(make_response({'message': 'Could not perform checkout'}, 400))
    get_customer_data_with_id(request_body['customer_id'])
    new_rental = Rental(
        customer_id = request_body['customer_id'],
        video_id = request_body['video_id'],
        )
    db.session.add(new_rental)
    db.session.commit()
    # maybe I can send args to 'to_dict' to customize what I need?
    # so we don't have code performing things in the model?
    return make_response(new_rental.to_dict(), 200)

# WHAT IF CUSTOMER HAS MULTIPLE OF THE SAME VIDEO CHECKED OUT
@rentals_bp.route('/check-in', methods=['POST'], strict_slashes=False)
def check_in_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    video = get_video_from_id(request_body['video_id'])
    get_customer_data_with_id(request_body['customer_id'])
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

# THIS ROUTE NEEDS TESTS
# GET /rentals/overdue
@rentals_bp.route('/overdue', methods=['GET'], strict_slashes=True)
def get_overdue_videos():
    overdue_movie_records = Rental.query.filter(Rental.checked_in==False and Rental.due_date<datetime.now()).all()
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