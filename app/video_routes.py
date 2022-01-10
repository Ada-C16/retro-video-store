from marshmallow import schema
from app import db
from app.customer_routes import validate_input
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
import requests, os, datetime
from datetime import timedelta

video_bp = Blueprint("videos", __name__, url_prefix="/videos")
from app.models.video import PutVideoInputSchema
put_video_schema = PutVideoInputSchema()

# creates a video
@video_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    request_data=request.get_json()

    if "title" not in request_data: 
        invalid_data={"details": "Request body must include title."}
        return jsonify(invalid_data),400
    if "release_date" not in request_data:
        invalid_data={"details": "Request body must include release_date."}
        return jsonify(invalid_data),400
    if "total_inventory" not in request_data:
        invalid_data={"details": "Request body must include total_inventory."}
        return jsonify(invalid_data),400
    
    new_video=Video(title=request_data["title"], release_date=request_data["release_date"], total_inventory=request_data["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

# lists all existing videos and details about each video
@video_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    videos_response = []
    videos = Video.query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200

# gives back details about specific video in the store's inventory
@video_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = validate_id(video_id)

    return jsonify(video.to_dict()), 200

# updates and return details about a specific video
@video_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def put_one_video(video_id): 
    video = validate_id(video_id)

    request_data=request.get_json()
    errors = put_video_schema.validate(request_data)

    if errors:
        return jsonify({"details": f"{errors} Invalid data"}),400
    else:
        video.title=request_data["title"]
        video.release_date=request_data["release_date"]
        video.total_inventory=request_data["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()),200

# deletes a specific video
@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = validate_id(video_id)

    if video.rentals:
        for rented_video in video.rentals:
            db.session.delete(rented_video)
            db.session.commit()
        return make_response("",200)
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}, 200

# list the customers who currently have the video checked out
@video_bp.route("<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_all_videos_rented(video_id):
    video_rented = validate_id(video_id)

    customer_list=[]
    for cust in video_rented.rentals:
        customer_list.append({
            "due_date": cust.due_date,
            "name":cust.customer.name,
            "phone": cust.customer.phone,
            "postal_code": cust.customer.postal_code
            })
    return jsonify(customer_list), 200        

# ************************************************* ENHANCEMENTS ************************************************

# lists customers that have checked out a copy of the video in the past
@video_bp.route("/<video_id>/history", methods=["GET"], strict_slashes=False)
def get_video_history(video_id):
    video = validate_id(video_id)

    video_history=[]

    for video in video.rentals:
        video_history.append({
        "customer_id": video.customer_id, 
        "name": video.customer.name,
        "postal_code": video.customer.postal_code, 
        "checkout_date": video.due_date-timedelta(days=7),
        "due_date": video.due_date })

    return jsonify(video_history), 200

# ********************************************** HELPER FUNCTIONS ***********************************************
def validate_id(id):
    try:
        id = int(id)
    except:
        abort(400, {"error": f"{id} must be numeric"})

    video = Video.query.get(id)
    if not video:
        abort(make_response({"message":f"Video {id} was not found"}, 404))
    return video