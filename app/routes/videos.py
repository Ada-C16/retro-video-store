
# ---------------------------------------
# ----------- VIDEOS SETUP --------------
# ---------------------------------------

## IN OTHER DOCS ##

# Set up the video model -> DONE
# Set up app.__init__.py (register blueprint)--> DONE

## IN THIS DOC ##

# Import necessary packages -> DONE
from flask import Blueprint, json, jsonify, request
from flask_sqlalchemy import _make_table
from app import db
from app.models.video import *
from app.helpers.videos import *

# Write blueprint for  video -> DONE
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


# ---------------------------------------
# ----------- VIDEOS ENDPOINTS ----------
# ---------------------------------------

# GET /videos Lists all existing videos and details about each video
# Return list of dictionaries of video data. Return empty array if no videos.
@videos_bp.route("", methods = ["GET"])
def get_videos():

    videos = Video.query.all()

    return list_of_videos(videos), 200

# POST /videos Creates a new video with given params:
#   title(str), release_date(datetime), total_inventory(int)
# Return dictionary with video data. "id" is the minimum required field tested for.
@videos_bp.route("", methods = ["POST"])
@require_valid_request_body
def add_new_video(request_body):

    new_video = Video()
    new_video.update_attributes(request_body)

    db.session.add(new_video)
    db.session.commit()

    return new_video.video_details(), 201

# GET /videos/<id> Gives back details about specific video.
# Return one dictionary of video's data.
@videos_bp.route("/<id>", methods = ["GET"])
@require_valid_id
def get_one_video(video):

    return video.video_details(), 200

# PUT /videos/<id> Updates and returns details about specific video
# Required request body params:
#   title(str), release_date(datetime), total_inventory(int)
# Return dictionary of video's updated data.
@videos_bp.route("<id>", methods = ["PUT"])
@require_valid_id
@require_valid_request_body
def update_video(video, request_body):

    video.update_attributes(request_body)

    db.session.commit()

    return video.video_details(), 200

# DELETE /video/<id> Deletes a specific video.
# Return dictionary with video data. "id" is the minimum required field tested for.
@videos_bp.route("<id>", methods = ["DELETE"])
@require_valid_id
def delete_video(video):

    db.session.delete(video)
    db.session.commit()

    return video.video_details(), 200