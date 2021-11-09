from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import requests

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')
video_bp = Blueprint('videos', __name__, url_prefix='/videos')

@video_bp.route('', methods=['GET', 'POST'])
def handle_videos():
    if request.method == 'GET':
        videos = Video.query.all()
        videos_list = [{"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory
                        } for video in videos]
        return jsonify(videos_list)
    elif request.method == 'POST':
        pass

@video_bp.route('/<video_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_one_video(video_id):
    # Even though the end-user may type a number as an argument for video_id, its data type isn't automatically int.
    # The try/except clause coerces the typed argument to be an int. If it is a non-numeric value, then a ValueError will be raised.
    # Alternatively, can also use isnumeric(). This will return a boolean, so no need for try/except. An if/else clause will suffice.
    try:
        id = int(video_id)
    except ValueError:
        return jsonify({"details": "Invalid data"}), 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    one_video = {"title": video.title,
                "id": video.id,
                "total_inventory": video.total_inventory}

    if request.method == 'GET':
        return one_video
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    
