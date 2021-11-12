from app import db
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from .helper_functions import *
from sqlalchemy.exc import DataError


videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('', methods=['GET'], strict_slashes=False)
def get_all_videos():
    sort_query = request.args.get("sort")
    responses_per_page = request.args.get("n", type=int)
    page = request.args.get("p", type=int)

    if sort_query:
        if sort_query == "title":
            videos = Video.query.order_by(Video.title.asc())
        elif sort_query == "release_date":
            videos = Video.query.order_by(Video.release_date.asc())
        elif sort_query == "total_inventory":
            videos = Video.query.order_by(Video.total_inventory.asc())
        if page and responses_per_page:
            videos = videos.paginate(page=page, per_page=responses_per_page)
            video_list = [video.to_dict() for video in videos.items]
            return make_response(jsonify(video_list), 200)
        video_list = [video.to_dict() for video in videos]
        return make_response(jsonify(video_list), 200)

    if page and responses_per_page:
        videos = Video.query.paginate(page=page, per_page=responses_per_page)
        video_list = [video.to_dict() for video in videos.items]
        return make_response(jsonify(video_list), 200)

    else:
        videos = Video.query.all()
        video_list =  [video.to_dict() for video in videos]
        return make_response(jsonify(video_list), 200)

    # videos = Video.query.all()
    # video_list =  [video.to_dict() for video in videos]
    # return make_response(jsonify(video_list), 200)

@videos_bp.route('', methods=['POST'], strict_slashes=False)
def create_video():
    request_body = request.get_json()
    confirm_all_video_fields_present(request_body)
    try:
        new_video = Video(
            title = request_body['title'],
            release_date = request_body['release_date'],
            total_inventory = request_body['total_inventory']
        )
        db.session.add(new_video)
        db.session.commit()
    except DataError:
        db.session.rollback()
        return make_response({'error':'Invalid data type in request body'}, 400)
    return make_response(new_video.to_dict(), 201)

# Individual video routes

@videos_bp.route('/<video_id>', methods=['GET'], strict_slashes=False)
def get_video(video_id):
    video = get_video_from_id(video_id)
    return make_response(video.to_dict(), 200)

@videos_bp.route('/<video_id>', methods=['PUT'], strict_slashes=False)
def update_video(video_id):
    video = get_video_from_id(video_id)
    request_body = request.get_json()
    confirm_all_video_fields_present(request_body)
    video.title = request_body['title']
    video.release_date = request_body['release_date']
    video.total_inventory = request_body['total_inventory']
    try:
        db.session.commit()
    except DataError:
        db.session.rollback()
        return make_response({'error':'Invalid data type in request body'}, 400)
    return make_response(video.to_dict(), 200)

@videos_bp.route('/<video_id>', methods=['DELETE'], strict_slashes=False)
def delete_video(video_id):
    video = get_video_from_id(video_id)
    db.session.delete(video)
    db.session.commit()
    return make_response(video.to_dict(), 200)

# Rental route
@videos_bp.route('/<id>/rentals', methods=['GET'], strict_slashes=False)
def get_customers_currently_with_video(id):
    # check if video exists
    get_video_from_id(id)
    rental_record = Rental.query.filter_by(video_id=id, checked_in=False).all()
    record_list = [record for record in rental_record]
    response = []
    for record in record_list:
        customer = Customer.query.get(record.customer_id)
        response.append({
            "due_date": record.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            })
    return make_response(jsonify(response), 200)