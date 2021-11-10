from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def valid_video(id):

    try:
        id = int(id)
    except ValueError:
        abort(400)

    video = Video.query.get(id)
    if video:
        return video

    abort(make_response({"message": f"Video {id} was not found"}, 404))


def missing_fields(request_body):

    required_fields = [
        "title",
        "release_date",
        "total_inventory",
    ]

    for field in required_fields:
        if field not in request_body:
            return {"details": f"Request body must include {field}."}
    return False


@videos_bp.route("", methods=["POST"])
def create_video():
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

        return make_response(missing_fields(request_body), 400)


@videos_bp.route("", methods=["GET"])
def get_all():

    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])


@videos_bp.route("/<id>", methods=["GET"])
def get_one(id):

    video = valid_video(id)
    return video.to_dict()


@videos_bp.route("/<id>", methods=["PUT"])
def update_video(id):

    video = valid_video(id)
    request_body = request.get_json()
    missing = missing_fields(request_body)

    if not missing:

        video.update(request_body)
        db.session.commit()
        return video.to_dict()

    else:
        abort(400)


@videos_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):

    video = valid_video(id)
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}
