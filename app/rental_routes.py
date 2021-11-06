from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, request
import os 

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rental_bp.route("", methods = ["GET", "POST"])
def handle_rentals():
    pass