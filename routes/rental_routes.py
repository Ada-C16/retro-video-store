from app import db
from app.models.customer import Customer
from datetime import date 
from flask import Blueprint, jsonify, request


rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
