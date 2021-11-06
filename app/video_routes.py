from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, request
import os 

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@video_bp.route("", methods = ["GET", "POST"])
def handle_videos():
    pass