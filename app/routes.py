from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request

customers_bp = Blueprint("customers", __name__, url_prefix="/cutsomers")

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass