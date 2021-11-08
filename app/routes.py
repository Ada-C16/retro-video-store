from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask_sqlalchemy import model
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.id,
                "title": video.title,
                "total_inventory": video.total_inventory,
                "release_date": video.release_date
            })
        return jsonify(videos_response)

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response ({"details": "Request body must include title."}), 400
        elif "release_date" not in request_body: 
            return make_response({"details":"Request body must include release_date."}, 400)
        elif "total_inventory" not in request_body:
            return make_response({"details":"Request body must include total_inventory."}, 400)
        
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
            )
        db.session.add(new_video)
        db.session.commit()
        
        response_body = {"id": new_video.id,
            "title": new_video.title,
            "release_date": new_video.release_date,
            "total_inventory": new_video.total_inventory}
            
        return jsonify(response_body), 201

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_video_by_id(video_id):
    try:
        int(video_id)
    except:
        return_message = {"message": f"Video {video_id} was not found"}
        return make_response(return_message, 400)

    video= Video.query.get(video_id)
    if video == None:
        return_message = {"message": f"Video {video_id} was not found"}
        return make_response(return_message, 404)

    if request.method == "PUT":
        form_data = request.get_json()
        try:
            form_data["title"]
            form_data["release_date"]
            form_data["total_inventory"]
        except:
            return make_response("You done goofed.", 400)
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        response_value = {
            "id": video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }
        return make_response(response_value, 200)



