from flask import Blueprint, json, jsonify, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from flask_sqlalchemy import model
from sqlalchemy import func
import requests

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def handle_rentals():
    request_body=request.get_json()
    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return make_response({"message":"Could not perform checkout"}, 404)
    elif not video:
        return make_response({"message":"Could not perform checkout"}, 404)
