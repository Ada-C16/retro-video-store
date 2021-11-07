from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from flask.json import tojson_filter
from flask.signals import request_tearing_down
from werkzeug.exceptions import RequestedRangeNotSatisfiable
from werkzeug.utils import header_property
from app.models.video import Video
from app import db
from datetime import datetime

video_bp = Blueprint("video", __name__, url_prefix="/videos")

# Helper Functions
def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_vidoe_from_id(video_id):
    valid_int(video_id, "video_id")
    return Video.query.get_or_404(video_id, description="{video not found}")


# Routes
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return make_response({"detail": "Invalid data"}, 400)
    
    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()

    return make_response({"video": new_video.to_dict()}, 201)