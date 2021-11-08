
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["POST","GET"])
def handle_videos():
    if request.method=="POST":
        request_body = request.get_json()
        if "total_inventory" not in request_body.keys(): 
            return make_response({"details": 'Request body must include total_inventory.'}, 400) 
        elif "release_date" not in request_body.keys(): 
            return make_response({"details":'Request body must include release_date.'}, 400) 
        elif "title" not in request_body.keys():
            return make_response({"details":'Request body must include title.'}, 400) 
        else:
            new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
            db.session.add(new_video)
            db.session.commit()
            return make_response({
                    "id": new_video.id,
                    "title": new_video.title,
                    "release_date": new_video.release_date,
                    "total_inventory": new_video.total_inventory
                }, 201)

    elif request.method=="GET":
        videos=Video.query.all()
        videos_response=[]
        for video in videos:
            videos_response.append({
                    "id": video.id,
                    "title": video.title,
                    "release_date": video.release_date,
                    "total_inventory": video.total_inventory
                })
        return jsonify(videos_response)

    
@videos_bp.route("<video_id>", methods=["GET", "PUT", "DELETE"])

def handle_a_video(video_id):
    
    if not video_id.isnumeric():
        return make_response({"details": "Invalid data"},400)
    video = Video.query.get(video_id)
    if video is None:
        return make_response({'message': f'Video {video_id} was not found'},404)

    elif request.method == "GET":
        return make_response({
                    "id": video.id,
                    "title": video.title,
                    "release_date":video.release_date,
                    "total_inventory": video.total_inventory})
                        
    elif request.method == "PUT":
        request_body = request.get_json()
        if "total_inventory" not in request_body.keys() or "release_date" not in request_body.keys() or "title" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400) 
        else:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
            db.session.commit()

            return make_response({
                        "id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory})

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({"id": video.id}, 200)