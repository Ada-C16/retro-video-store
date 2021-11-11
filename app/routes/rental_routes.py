from flask import Blueprint, request, make_response, abort
from app.models.rental import Rental
from app.models.video import Video
from app.models.customer import Customer
from app import db

#helper functions
def validate_id(id, id_type):
    try:
        int(id)
    except:
        abort(make_response({"error": f"{id_type} must be an int"}, 400))

def get_video_from_id(id):
    validate_id(id, 'video id')
    selected_video = Video.query.get(id)
    if not selected_video:
        abort(make_response({'message': f'Video {id} was not found'}, 404))
    return selected_video

def get_customer_data_with_id(customer_id):
    validate_id(customer_id, "id")
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

    return customer

# Blueprint
rentals_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

@rentals_bp.route('/check-out', methods=['POST'], strict_slashes=False)
def check_out_movie():
    request_body = request.get_json()
    if 'customer_id' not in request_body or 'video_id' not in request_body:
        abort(make_response({'error': 'customer_id and video_id are required'}, 400))
    video = get_video_from_id(request_body['video_id'])
    # check if inventory is non-zero
    if video.total_inventory < 1:
        abort(make_response({'message': 'Could not perform checkout'}, 400))
    get_customer_data_with_id(request_body['customer_id'])
    new_rental = Rental(
        customer_id = request_body['customer_id'],
        video_id = request_body['video_id'],
        )
    video.total_inventory -= 1
    db.session.add(new_rental)
    db.session.commit()
    return make_response(new_rental.to_dict(), 200)
