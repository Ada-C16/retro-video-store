from flask import Blueprint, jsonify
from app import db
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
