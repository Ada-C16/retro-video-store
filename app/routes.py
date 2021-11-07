import os
import requests
from sqlalchemy.orm import query
from app import db
from datetime import datetime
from dotenv import load_dotenv
from app.models.rental import Rental
from app.models.video import Video
from app.models.video import Customer
from flask import Blueprint ,jsonify, request

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customer", __name__, url_prefix="/customers")