from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video

video_bp = Blueprint('videos', __name__, url_prefix='/videos')

@video_bp.route('', methods=['GET'])
def read_all_videos():
    videos = Video.query.all()

    response_body = [video.to_dict() for video in videos]
    return make_response(jsonify(response_body), 200)

# @video_routes('/<video_id>', methods=['GET'])
# def read_single_video(video_id):
#     video = Video.query.get(video_)