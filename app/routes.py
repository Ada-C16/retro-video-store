from flask import Blueprint, jsonify, make_response, request, abort
from werkzeug.exceptions import NotFound
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timezone
import requests
import os

#DEFINE BLUEPRINTS
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#----------- HELPER FUNCTIONS -----------
def validate_video_id(video_id):
    try: 
        video_id == int(video_id)
    except:
        abort(400, {"message": f"video {video_id} was not found"})
    return Video.query.get_or_404(video_id)

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

#----------- GET ---------------------
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response=[]
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    try:
        video = validate_video_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Video {id} was not found"}), 404)
    return jsonify(video.to_dict())

#---------- UPDATE -----------------

@video_bp.route("/<id>", methods=["PUT"])
def update_video(id):
    try:
        video = validate_video_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Video {id} was not found"}), 404)
    request_body = request.get_json()

    if request_body.get("title") and request_body.get("release_date") and request_body.get("total_inventory"):
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    else:
        return make_response((jsonify({"message": f"Attribute missing from video"}), 400))
    # if request_body.get("title"):
    #     video.title = request_body["title"]
    # if request_body.get("release_date"):
    #     video.release_date = request_body["release_date"]
    # if request_body.get("total_inventory"):
    #     video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return video.to_dict()

#--------- DELETE ------------------
@video_bp.route("/<id>",methods=["DELETE"])
def delete_video(id):
    try:
        video = validate_video_id(id)
    except NotFound:
        return make_response(jsonify({"message": f"Video {id} was not found"}), 404)
    video = video.query.get(id)
    db.session.delete(video)
    db.session.commit()

    response_body = ({'id':video.id, 'details' : f'Video {video.id} successfully deleted'})
    return make_response(response_body, 200)