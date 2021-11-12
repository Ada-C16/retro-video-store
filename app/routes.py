from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.validate import Validate

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
