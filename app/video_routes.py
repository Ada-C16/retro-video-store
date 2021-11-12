from app import db
from app.models.video import Video
from app.models.customer import Customer
from flask import request, Blueprint, jsonify


import requests

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")



@videos_bp.route("", methods=["POST", "GET"])
def handle_videos():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify(details="Request body must include title."), 400
        elif "release_date" not in request_body:
            return jsonify(details="Request body must include release_date."), 400
            
        elif "total_inventory" not in request_body:
            return jsonify(details="Request body must include total_inventory."), 400
        new_video=Video.from_json(request_body)


        db.session.add(new_video)
        db.session.commit()

        return jsonify(new_video.to_json()), 201

    elif request.method == "GET":
        videos = Video.query.all()
        response_body = []
        for video in videos:
            response_body.append(video.to_json())

        return jsonify(response_body), 200


@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_video(video_id):
    if not video_id.isnumeric():
        return jsonify(""), 400

    video = Video.query.get(video_id)

    if video:
        if request.method == "GET":
            return jsonify(video.to_json()), 200
    
    
    
        elif request.method == "PUT":
            request_body = request.get_json()
            if "title" not in request_body:
                return jsonify(""), 400
            elif "release_date" not in request_body:
                return jsonify(""), 400
            elif "total_inventory" not in request_body:
                return jsonify(""), 400
            elif type(request_body["total_inventory"]) != int:   
                return jsonify(""), 400

                
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
            db.session.commit()
            return jsonify(video.to_json()), 200

        elif request.method == "DELETE":
            db.session.delete(video)
            db.session.commit()
            return jsonify(id=video.id), 200
    else:
        return jsonify(message=f"Video {video_id} was not found"), 404

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def handle_video_rentals(video_id):
    if not video_id.isnumeric():
        return jsonify("Video id must be an integer"), 400

    video = Video.query.get(video_id)
    if video:
        customers = video.customers
        customers_response = [customer.to_json() for customer in customers]
        return jsonify(customers_response), 200
    else:
        return jsonify(message=f"Video {video_id} was not found"), 404