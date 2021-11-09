from flask import Blueprint, jsonify, request, make_response, abort
from app.models.customer import Customer
from app.models.video import Video
from app import db
import requests
from dotenv import load_dotenv

#Video blueprint

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

#Videos routes

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):

    video_id = is_id_valid(video_id)
    video = Video.query.get(video_id)

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 
    else:
        return make_response(jsonify(video.to_dict()), 200)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 
    else:
        db.session.delete(video)
        db.session.commit()
        return make_response(jsonify({"id": int(video_id)}), 200)

@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = video_has_required_attributes(request.get_json())

    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"]    
)
    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    request_body = video_has_required_attributes(request.get_json())

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    db.session.commit()

    return make_response(jsonify(video.to_dict()), 200)


#Helper Functions

def is_id_valid(video_id):
    try:
        int(video_id)
    except:
        abort(make_response(jsonify({"message": "Please input valid id number"}), 400))
    return video_id

def video_has_required_attributes(request_body):
    required_attributes = ["title", "release_date", "total_inventory"]
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {attribute}."}), 400))
    return request_body


#Customer Blueprint

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers Routes

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)
