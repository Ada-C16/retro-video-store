from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask_sqlalchemy import model
from sqlalchemy import func
import requests
from datetime import timedelta

from tests.test_wave_02 import CUSTOMER_NAME


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
            
        return jsonify(new_video.create_video_dict()), 201

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

        return make_response(video.create_video_dict(), 200)


    if request.method == "GET":
        return make_response(video.create_video_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({"id":int(video_id)}, 200)

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def handle_rental_by_video_id(video_id):
    try:
        int(video_id)
    except:
        return_message = {"message": f"Video {video_id} was not found"}
        return make_response(return_message, 404)
    
    video= Video.query.get(video_id)
    if not video:
        return_message = {"message": f"Video {video_id} was not found"}
        return make_response(jsonify(return_message), 404)

    from app.models.rental import Rental
    video_rentals = Rental.query.filter_by(video_id = video.id).all()
    rentals_output_list = []
    for num, rental in enumerate(video_rentals):
        customer = Customer.query.filter_by(id = rental.customer_id).first()
        rentals_output_list.append(rental.create_dict())

    return make_response(jsonify(rentals_output_list), 200)