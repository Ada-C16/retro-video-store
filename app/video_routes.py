from app import db
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('', methods=['GET', 'POST'])
def handle_videos():
    if request.method == 'GET':
        videos = Video.query.all()
        return jsonify([video.to_dict() for video in videos]), 200

    elif request.method == 'POST':
        request_body = request.get_json()
        #checks for list if we want to post multiple videos
        if isinstance(request_body, list):
            for video in request_body:
                new_video = Video(
                    title = video['title'],
                    release_date = video['release_date'],
                    total_inventory = video['total_inventory']
                )
                db.session.add(new_video)
                return jsonify({"video": video.to_dict()} for video in request_body), 201
        else:
            new_video = Video(
                title = request_body['title'],
                release_date = request_body['release_date'],
                total_inventory = request_body['total_inventory']
            )
            db.session.add(new_video)
            return jsonify({"video": new_video.to_dict()}), 201

@videos_bp.route('/<id_num>', methods=['GET', 'PUT', 'DELETE'])
def handle_video(id_num):
    try:
        id_num = int(id_num)
    except ValueError:
        return make_response(jsonify({"error": "Invalid ID"}), 400)

    video = Video.query.get(id_num)
    if not video:
        return make_response(jsonify({"message": f"Video {id_num} was not found"}), 404)
    
    if request.method == 'GET':
        return jsonify(video.to_dict()), 200

    elif request.method == 'PUT':
        request_body = request.get_json()
        for key, value in request_body.items():
            if key in Video.__table__.columns.keys():
                setattr(video, key, value)
        db.session.commit()
        return jsonify({"video": video.to_dict()}), 200
    
    elif request.method == 'DELETE':
        video_id = video.to_dict()['id']
        video_title = video.to_dict()['title']

        db.session.delete(video)
        db.session.commit()
        return jsonify({"details": f"Video {video_title} with id {video_id} was deleted"}), 200


