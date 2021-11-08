from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import datetime
import requests, os
from dotenv import load_dotenv

video_bp = Blueprint('video', __name__, url_prefix="/videos")
customer_bp = Blueprint('customer', __name__, url_prefix="/customers")
load_dotenv()