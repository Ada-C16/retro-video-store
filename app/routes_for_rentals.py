from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask_sqlalchemy import model
from sqlalchemy import func
import requests

rentals_bp = Blueprint("videos", __name__, url_prefix="/rentals")