from app import db
from app.models.video import Video
from flask import Blueprint, json, jsonify, request
from app.models.video import video
from datetime import datetime
import requests
import os

from tests.test_wave_01 import video_NAME

video_bp = Blueprint("videos", __name__, url_prefix=("/videos"))


@video_bp.route("", methods=["GET"])
def get_video():
    if request.method == "GET":
        videos = Video.query.all()
        video_response = []
        for video in videos:
            video_response.append(
                {
                    "id": video.video_id,
                    "title": video.video_title,
                    "total_inventory": video.video_inventory,
                }
            )
    return jsonify(video_response), 200


@video_bp.route("", methods=["POST"])
def put_video():
    if request.method == "POST":
        request_body = request.get_json()

        if "name" not in request_body:
            return jsonify({"details": "Request body must include name."}), 400

        if "postal_code" not in request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400

        if "phone" not in request_body:
            return jsonify({"details": "Request body must include phone."}), 400

        else:

            new_video = video(
                name=request_body["name"],
                phone=request_body["phone"],
                postal_code=request_body["postal_code"],
            )

            db.session.add(new_video)
            db.session.commit()

            return jsonify(new_video.video_information()), 201


@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def gpd_video(video_id):
    video = video.query.get(video_id)
    if video == None:
        return (
            jsonify({"message": f"video {video_id} was not found"}),
            404,
        )

    if request.method == "GET":

        video_response = {
            "id": video.video_id,
            "name": video.name,
            "postal_code": video.postal_code,
            "phone": video.phone,
        }

        return jsonify(video_response), 200

    if request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body:
            return jsonify(None), 400
        if "postal_code" not in request_body:
            return jsonify(None), 400
        else:
            form_data = request.get_json(video_id)
            video.name = form_data["name"]
            video.phone = form_data["phone"]
            video.postal_code = form_data["postal_code"]

            db.session.commit()

            return (
                jsonify(
                    "/{video_name}/{video_id}",
                    {
                        "name": f"Updated ${video.name}",
                        "phone": f"Updated ${video.phone}",
                        "postal_code": f"Updated ${video.postal_code}",
                    },
                )
            ), 200

    elif request.method == "DELETE":
        db.session.delete(video_id)
        db.session.commit()
        return jsonify({"id": None}), 200


@video_bp.route("/hello", methods=["GET"])
def get_hello():
    return jsonify(None), 400
