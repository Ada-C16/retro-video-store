from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timezone
import requests
import os

#DEFINE BLUEPRINTS
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#----------- CREATE ---------------------
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response(jsonify({"details" : "Request body must include title."}), 400)
    if "release_date" not in request_body:
        return make_response(jsonify({"details" : "Request body must include release_date."}), 400)
    if "total_inventory" not in request_body:
        return make_response(jsonify({"details" : "Request body must include total_inventory."}), 400)
    
    new_video = Video(
        title=request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
    )

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()),201)
