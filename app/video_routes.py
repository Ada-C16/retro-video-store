from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, request, jsonify
import os 

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@video_bp.route("", methods = ["GET","POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        response_body = build_videos_response(videos)
        return jsonify(response_body),200

    if request.method == "POST":
        request_body = request.get_json()
        valid_request = "title" in request_body and "total_inventory"\
            in request_body and "release_date" in request_body
        
        if not valid_request:
            response = build_invalid_post_response(request_body)
            return response
        else : 
            new_video = Video(
                title = request_body["title"],
                release_date = request_body["release_date"],
                total_inventory = request_body["total_inventory"]
            )
            db.session.add(new_video)
            db.session.commit() 
            response_body = build_video_response(new_video)
            return jsonify(response_body), 201


@video_bp.route("<video_id>", methods = ["GET","PUT","DELETE"])
def handle_video (video_id): 
    # have to check before query otherwise get a data error
    if not video_id.isnumeric():
        return jsonify({"details": "id must be numerical"}),400
    
    video = Video.query.get(video_id)
    if video == None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    
    #method request#
    #GET
    if request.method == "GET":
        response_body = build_video_response(video)
        return jsonify(response_body), 200

    #PUT
    if request.method == "PUT":
        request_body = request.get_json()
        valid_request = "title" in request_body and "total_inventory" in request_body and \
            "release_date" in request_body
        if not valid_request:
            response = build_invalid_post_response(request_body)
            return response
        else:
            video.title = request_body["title"],
            video.release_date = request_body["release_date"],
            video.total_inventory = request_body["total_inventory"]
            
            db.session.commit()
            response_body = build_video_response(video)
            return jsonify(response_body), 200

    #DELETE
    if request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        response_body = build_video_response(video)
        return jsonify(response_body), 200

##HELP##
def build_videos_response(videos):
    response = []
    for video in videos:
        response.append({
        "id": video.id, 
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory
        })
    return response 
    
def build_video_response(video):
    response = {
        "id": video.id, 
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory
        }
    return response

def build_invalid_post_response(request_body):
    response = {}
    if "title" not in request_body :
        response = {"details": "Request body must include title."}, 400

    if "total_inventory" not in request_body:
        response = {"details":"Request body must include total_inventory."}, 400

    if "release_date" not in request_body:
        response = {"details":"Request body must include release_date."}, 400
    return response
