from flask import Blueprint, jsonify, request, abort
from flask.helpers import make_response
from app.models.video import Video
from app import db

# helper functions
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

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('', methods=['GET'], strict_slashes=False)
def get_all_videos():
    videos = Video.query.all()
    video_list =  [video.to_dict() for video in videos]
    return make_response(jsonify(video_list), 200)

@videos_bp.route('', methods=['POST'], strict_slashes=False)
def create_video():
    request_body = request.get_json()
    missing_fields = []
    if 'title' not in request_body:
        missing_fields.append('Request body must include title.')
    if 'release_date' not in request_body:
        missing_fields.append('Request body must include release_date.')
    if 'total_inventory' not in request_body:
        missing_fields.append('Request body must include total_inventory.')
    if missing_fields:
        return make_response({'details': missing_fields}, 400)
    new_video = Video(
        title = request_body['title'],
        release_date = request_body['release_date'],
        total_inventory = request_body['total_inventory']
    )
    db.session.add(new_video)
    db.session.commit()
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
    # check if request body is valid
    if 'title' not in request_body or 'release_date' not in request_body or 'total_inventory' not in request_body:
        abort(make_response(jsonify('Bad request'), 400))
    video.title = request_body['title']
    video.release_date = request_body['release_date']
    video.total_inventory = request_body['total_inventory']
    db.session.commit()
    return make_response(video.to_dict(), 200)

@videos_bp.route('<video_id>', methods=['DELETE'], strict_slashes=False)
def delete_video(video_id):
    video = get_video_from_id(video_id)
    db.session.delete(video)
    db.session.commit()
    return make_response(video.to_dict(), 200)