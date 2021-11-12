from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.video import Video
from app.validate import Validate

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@videos_bp.route("", methods=["POST"])
def create_video():  # Do the same thing has routes with video and customer, make class methods and combine routes
    request_body = request.get_json()
    try:
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"],
        )
        db.session.add(new_video)
        db.session.commit()

        return new_video.to_dict(), 201

    except KeyError:

        return make_response(Validate.missing_fields(request_body, Video), 400)


@videos_bp.route("", methods=["GET"])
def get_all():

    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])


@videos_bp.route("/<id>", methods=["GET"])
def get_one(id):
    video_id = Validate.valid_id(id)
    video = Validate.valid_video(video_id)

    return video.to_dict()


@videos_bp.route("/<id>", methods=["PUT"])
def update_video(id):

    video_id = Validate.valid_id(id)
    video = Validate.valid_video(video_id)
    request_body = request.get_json()
    missing = Validate.missing_fields(request_body, Video)

    if not missing:

        video.update(request_body)
        db.session.commit()
        return video.to_dict()

    else:
        abort(400)


@videos_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):

    video_id = Validate.valid_id(id)
    video = Validate.valid_video(video_id)
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}


@videos_bp.route("/<id>/rentals", methods=["GET"])
def current_rentals(id):

    video_id = Validate.valid_id(id)
    video = Validate.valid_video(video_id)

    rentals = video.get_customers()
    return jsonify(rentals), 200
