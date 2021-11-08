from flask import Blueprint
# GET /videos
# GET /videos/<id>
# POST /videos
# PUT /videos/<id>
# DELETE /videos/<id>

videos_bp = Blueprint('videos', __name__, url_prefix='/videos')
