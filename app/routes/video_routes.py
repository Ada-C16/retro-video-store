from flask import Blueprint, jsonify, request
from flask.helpers import make_response
from app.models.video import Video
from app import db
# GET /videos
# GET /videos/<id>
# POST /videos
# PUT /videos/<id>
# DELETE /videos/<id>

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
