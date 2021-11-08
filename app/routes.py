from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from dotenv import load_dotenv
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

