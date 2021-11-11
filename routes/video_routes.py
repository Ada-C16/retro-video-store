from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
from flask import Blueprint, jsonify, request


video_bp = Blueprint("videos", __name__, url_prefix=("/videos"))


@video_bp.route("", methods=["GET"])
def get_video():
    """
    Retrieves all saved video records
    """
    video = Video.query.all()
    video_response = [video.to_json() for video in video]
    return jsonify(video_response), 200


# post a video
@video_bp.route("", methods=["POST"])
def post_video():
    """
    Allows client to create new video records,
    which must have title, release_date, and
    total_inventory
    """
    if request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body:
            return jsonify(details="Request body must include title."), 400

        if "release_date" not in request_body:
            return jsonify(details="Request body must include release_date."), 400

        if "total_inventory" not in request_body:
            return jsonify(details="Request body must include total_inventory."), 400

        new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory = request_body["total_inventory"]
        )

        db.session.add(new_video)
        db.session.commit()

        return {
            "id": new_video.id,
            "title": new_video.title,
            "release_date": new_video.release_date,
            "total_inventory": new_video.total_inventory
        }, 201



@video_bp.route("/<video_id>", methods=["GET","PUT","DELETE"])
def handle_video_id(video_id):
    """
    Allows client to retrieve, post, and delete video records
    only after ensuring that the video_id is an integer.
    """
    try: 
        video_id = int(video_id)
    except:
        return jsonify(None), 400

    video = Video.query.get(video_id)


    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    elif request.method == "GET":
        return {
            "id": video.id,
            "title": video.title,
            "total_inventory": video.total_inventory
        }, 200


    elif request.method == "PUT":
        form_data = request.get_json()

        if "title" not in form_data or "release_date" not in form_data \
        or "total_inventory" not in form_data:
            return jsonify(None), 400

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return {
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }, 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return {
            "id": video.id
        }, 200