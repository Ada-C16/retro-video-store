from app import db
from app.models.customer import Customer
from datetime import date
from app.models.rental import Rental
from app.models.video import Video
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request


rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rental_bp.route("/check-out", methods=["POST"])
def rental_check_out():
    pass
