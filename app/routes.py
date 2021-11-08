from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
@videos_bp.route("", methods=["POST"])
def post_videos():
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