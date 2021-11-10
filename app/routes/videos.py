# ---------------------------------------
# ----------- VIDEOS SETUP ----------
# ---------------------------------------

## IN OTHER DOCS ##

# Set up the video model -> DONE
# Set up app.__init__.py (register blueprint)--> DONE

## IN THIS DOC ##

# Import necessary packages -> DONE
from flask import Blueprint, json, jsonify, request
from flask_sqlalchemy import _make_table
from app import db
from app.models.video import Video

# Write blueprint for  video -> DONE
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


# ---------------------------------------
# ----------- VIDEOS ENDPOINTS ----------
# ---------------------------------------

# GET /videos Lists all existing videos and details about each video
# Successful response status: 200
# If no videos, return empty array and 200 status
# Return list of dictionaries of video data.
@videos_bp.route("", methods = ["GET"])
def get_videos():

    videos = Video.query.all()

    return jsonify(list_of_videos(videos)), 200


# POST /videos Creates a new video with given params:
#   title(str), release_date(datetime), total_inventory(int)
# Successful response status: 201:Created
# Error status: 400: Bad request. Provide details of error if invalid input.
# Return dictionary with video data. "id" is the minimum required field tested for.
@videos_bp.route("", methods = ["POST"])
def add_new_video():
    
    request_body = request.get_json()
    
    ### Opportunity to use the invalid input decorator here if we figure out how to create one! ###
    if is_invalid(request_body):
        return is_invalid(request_body)

    new_video = Video(title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return video_details(new_video), 201


# GET /videos/<id> Gives back details about specific video.
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if video does not exist.
# Return one dictionary of video's data.
@videos_bp.route("/<id>", methods = ["GET"])
def get_one_video(id):

    try:
        id = int(id)
    except ValueError:
        return {"message": "Video id needs to be an integer"}, 400

    video = Video.query.get(id)
    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    return video_details(video), 200

# PUT /videos/<id> Updates and returns details about specific video
# Required request body params:
#   title(str), release_date(datetime), total_inventory(int)
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if video does not exist.
# Error status: 400: Bad request. Provide details of error if invalid input.
# Return dictionary of video's updated data.
@videos_bp.route("<id>", methods = ["PUT"])
def update_video(id):

    try:
        id = int(id)
    except ValueError:
        return {"message": "Video id needs to be an integer"}, 400

    request_body = request.get_json()

    ### Opportunity to use the invalid input decorator here if we figure out how to create one! ###
    if is_invalid(request_body):
        return is_invalid(request_body)

    video = Video.query.get(id)

    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    video.title =request_body["title"]
    video.release_date=request_body["release_date"]
    video.total_inventory=request_body["total_inventory"]

    db.session.commit()

    return request_body, 200

# DELETE /video/<id> Deletes a specific video.
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if video does not exist.
# Return dictionary with video data. "id" is the minimum required field tested for.
@videos_bp.route("<id>", methods = ["DELETE"])
def delete_video(id):

    try:
        id = int(id)
    except ValueError:
        return {"message": "Video id needs to be an integer"}, 400

    video = Video.query.get(id)
    if not video: 
        return {"message": f"Video {id} was not found"}, 404
    
    db.session.delete(video)
    db.session.commit()

    return video_details(video), 200


def video_details(video):
    return {
    "id": video.id,
    "title": video.title,
    "release_date": video.release_date,
    "total_inventory": video.total_inventory
    } 

def list_of_videos(videos):
    return [video_details(video) for video in videos]


def is_invalid(request_body):
    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    elif "release_date" not in request_body:
        return {"details": "Request body must include release_date."}, 400
    elif "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400
    