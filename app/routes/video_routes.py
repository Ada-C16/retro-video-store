
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():
    
    if request.method == "GET":
        sort_query = request.args.get("sort")
        
        if sort_query == "asc":
            videos = Video.query.order_by(Video.title.asc())
         
        elif sort_query == "desc":
            videos = Video.query.order_by(Video.title.desc())
            
        else:
            videos = Video.query.all()

        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            })

        return jsonify(videos_response), 200


    elif request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:

            return jsonify({
                "details": "Invalid data"
            }), 400

        new_video = Video(title=request_body["title"], total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"])

        db.session.add(new_video)
        db.session.commit()
       
       
        return jsonify(
            {
                "id": new_video.id
            }), 201

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response(f"Video {video_id} not found", 404)

    if request.method == "GET":
        # if video.goal_id:
        #     return {
        #     "task": {
        #         "id": video.id,
        #         "goal_id": task.goal_id,
        #         "title": task.title,
        #         "description": task.description,
        #         "is_complete": task.completed_at != None  
        #         }
        #     }
        # else:
        return jsonify({
            
                "id": video.id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory   
                
            }), 200
    
    elif request.method == "PUT":
        form_data = request.get_json()

        if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:

            return jsonify({
                "details": "Invalid data"
            }), 400

        #add code for edge case where inputs all there but one or more=invalid, for example toatal inventory is not an integer

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return jsonify({
        
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory  
            
        })

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return jsonify({
            "details": (f'Video {video.id} "{video.title}" successfully deleted')
            })


