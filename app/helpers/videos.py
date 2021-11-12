from functools import wraps
from app.models.video import Video
from flask import jsonify, request

# Decorator to check if id is an integer and if the video exists.
def require_valid_id(endpoint):
    @wraps(endpoint)
    def fn(*args, id, **kwargs):
        try:
            id = int(id)
        except ValueError:
            return {"message": "Video id needs to be an integer"}, 400

        video = Video.query.get(id)

        if not video: 
            return {"message": f"Video {id} was not found"}, 404

        return endpoint(*args, video=video, **kwargs)
    return fn

# Decorator to check if the request_body includes name, postal_code, and phone.
def require_valid_request_body(endpoint):
    @wraps(endpoint)
    def fn(*args, **kwargs):
        request_body = request.get_json()

        if "title" not in request_body:
            return {"details": "Request body must include title."}, 400
        elif "release_date" not in request_body:
            return {"details": "Request body must include release_date."}, 400
        elif "total_inventory" not in request_body:
            return {"details": "Request body must include total_inventory."}, 400
        else:
            return endpoint(*args, request_body=request_body, **kwargs)
    return fn

def list_of_videos(videos):
    return jsonify([video.video_details() for video in videos])
