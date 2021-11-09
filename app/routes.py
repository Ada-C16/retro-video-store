from flask import Blueprint, jsonify, request, make_response, abort
from app.models.video import Video
from app.models.customer import Customer
from app import db
from sqlalchemy import desc
from datetime import date, time, datetime
import requests
import os

# assign videos_bp to the new Blueprint instance
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# beginning CRUD routes/ endpoints for videos
@videos_bp.route("", methods=["POST"])
def post_one_video():
# request_body will be the user's input, converted to json. it will be a new record 
# for the db, with all fields (a dict)
    request_body = request.get_json()
# this guard clause will give an error if user tries to submit request body that does
# not have all fields present
    if 'title' not in request_body:
        return make_response({"details": "Request body must include title."}, 400)
    elif 'release_date' not in request_body:
        return make_response({"details": "Request body must include release_date."}, 400)
    elif 'total_inventory' not in request_body:
        return make_response({"details": "Request body must include total_inventory."}, 400)
    else:
# taking info fr request_body and converting it to new Video object    
        new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
# committing changes to db
        db.session.add(new_video)
        db.session.commit()
# return formatted response body
        return make_response({ "id": new_video.id,
                                        "title": new_video.title,
                                        "release_date": new_video.release_date,
                                        "total_inventory": new_video.total_inventory}, 201)

@videos_bp.route("", methods=["GET"])
def get_all_videos():
# querying db for all videos and ordering them by title, then storing that list of 
# objects in local videos variable    
    videos = Video.query.order_by(Video.title).all()
    videos_response = []
    # looping through eachvideo, converting to requested format (dict) and adding to
    # videos_response which will be list of dicts
    for video in videos:    
        videos_response.append({
        'id':video.id,
        'title':video.title,
        'release_date':video.release_date,
        'total_inventory':video.total_inventory
        })
    
    return jsonify(videos_response), 200
