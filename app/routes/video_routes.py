from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.video import Video, video_from_json
from app.routes.route_helpers import invalid_id, invalid_request_body

video_bp = Blueprint('videos', __name__, url_prefix='/videos')

@video_bp.route('', methods=['GET'])
def read_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return make_response(jsonify(response_body), 200)

@video_bp.route('', methods=['POST'])
def create_new_video():
    request_body = request.get_json()
    required_keys = ['title', 'release_date', 'total_inventory']
    if invalid_request_body(request_body, required_keys):
        return invalid_request_body(request_body, required_keys)

    video_to_create = video_from_json(request_body)
    db.session.add(video_to_create)
    db.session.commit()

    response_body = video_to_create.to_dict()
    return make_response(jsonify(response_body), 201)

@video_bp.route('/<video_id>', methods=['GET'])
def read_single_video(video_id):
    if invalid_id(video_id):
        return invalid_id(video_id)

    video = Video.query.get(video_id)
    try:
        response_body = video.to_dict()
        return make_response(jsonify(response_body), 200)
    except AttributeError:
        response_body = {'message': f'Video {video_id} was not found'}
        return make_response(jsonify(response_body), 404)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def read_one_video_rentals(video_id):
    if invalid_id(video_id):
        return invalid_id(video_id)

    video = Video.query.get(video_id)

    if not video:
        return {"message": f"Video {video_id} was not found"}, 404        

    rentals = video.rentals
    response_body  = [rental.get_customer() for rental in rentals]
    return make_response(jsonify(response_body), 200)

@video_bp.route('/<video_id>', methods=['PUT'])
def update_single_video(video_id):
    if invalid_id(video_id):
        return invalid_id(video_id)

    video_to_update = Video.query.get(video_id)
    try:
        request_body = request.get_json()
        required_keys = ['title', 'release_date', 'total_inventory']
        if invalid_request_body(request_body, required_keys):
            return invalid_request_body(request_body, required_keys)
        
        video_to_update.title = request_body['title']
        video_to_update.release_date = request_body['release_date']
        video_to_update.total_inventory = request_body['total_inventory']
        db.session.commit()
        response_body = video_to_update.to_dict()
        return make_response(jsonify(response_body), 200)
    except AttributeError:
        response_body = {'message': f'Video {video_id} was not found'}
        return make_response(jsonify(response_body), 404)

@video_bp.route('/<video_id>', methods=['DELETE'])
def delete_single_video(video_id):
    if invalid_id(video_id):
        return invalid_id(video_id)

    video_to_delete = Video.query.get(video_id)
    if not video_to_delete:
        response_body = {'message': f'Video {video_id} was not found'}
        return make_response(jsonify(response_body), 404)
    db.session.delete(video_to_delete)
    db.session.commit()
    response_body = video_to_delete.to_dict()
    return make_response(jsonify(response_body), 200)
    