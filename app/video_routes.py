from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def validate(id):

    try:
        id = int(id)
    except ValueError:
        abort(400)
    return Video.query.get_or_404(id)


@videos_bp.route("", methods=["GET"])
def get_all():

    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])


@videos_bp.route("", methods=["GET"])
def get_one(id):

    video = validate(id)
    return video.to_dict()
