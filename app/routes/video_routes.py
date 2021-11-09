from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app import db
from datetime import date
import requests
import os
TOKEN = os.environ.get('TOKEN')

video_bp = Blueprint("video", __name__, url_prefix="/videos")


###REGISTER BLUEPRINT???

# Helper Functions
def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_video_from_id(video_id):
    valid_int(video_id, "video_id")
    return Video.query.get_or_404(video_id)

@video_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify({"message":f"Video 1 was not found"}), 404

# Routes

@video_bp.route("", methods=['POST'])
def create_video():
    """CREATES new video in database"""
    request_body = request.get_json()

    if "title" not in request_body:
         return {"details" : f"Request body must include title."}, 400

    if "release_date" not in request_body:
        return {"details" : f"Request body must include release_date."}, 400

    if "total_inventory" not in request_body:
        return {"details" : f"Request body must include total_inventory."}, 400

    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()
    return new_video.to_dict(), 201


@video_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    """READS video with given id"""
    video = get_video_from_id(video_id)

    return video.to_dict(), 200


@video_bp.route("", methods=["GET"])
def get_videos():
    """READS all videos"""

    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(
            video.to_dict()
        )
    return jsonify(videos_response), 200


@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """UPDATES video with given id"""
    if video_id == None:
        return make_response(404)

    else:
        video = get_video_from_id(video_id)
        request_body = request.get_json()

        if "title" not in request_body:
            return {"details" : f"Request body must include title."}, 400           
        if "release_date" not in request_body:
            return {"details" : f"Request body must include release_date."}, 400
        if "total_inventory" not in request_body:
            return {"details" : f"Request body must include total_inventory."}, 400

        video.title = request_body["title"]
        video.release_date = request_body["release_date"]    
        video.total_inventory = request_body["total_inventory"]

        video_response = video.to_dict()

        db.session.commit()
        return video_response, 200


@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    """DELETES video with given id"""
    video = get_video_from_id(video_id)

    db.session.delete(video)
    db.session.commit()
    return video.to_dict(), 200


