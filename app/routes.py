from flask import Blueprint, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
import requests
import os
from dotenv import load_dotenv

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers Routes

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)
