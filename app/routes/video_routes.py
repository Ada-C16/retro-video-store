from flask import Blueprint, jsonify
from flask.helpers import make_response
from app.models.video import Video
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