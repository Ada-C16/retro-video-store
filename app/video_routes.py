from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def valid_id(id):

    try:
        id = int(id)
    except ValueError:
        abort(400)
    return Video.query.get(id)


def get_video(id):

    video = valid_id(id)
    if not video:
        abort(make_response({"message": f"Video {id} was not found"}, 404))
    return video


@videos_bp.route("", methods=["GET"])
def get_all():

    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])


@videos_bp.route("/<id>", methods=["GET"])
def get_one(id):

    video = get_video(id)
    return video.to_dict()
