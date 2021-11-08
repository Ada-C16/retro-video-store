from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime

# setup blueprints here
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers routes

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    # response = []
    customers = Customer.query.all()
    # for customer in customers:
    #     response.append(customer.to_dict())

    response = [customer.to_dict() for customer in customers]

    return jsonify(response)

