from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# HELPER FUNCTIONS

# CUSTOMER ROUTES

# Get all customers
@customer_bp.route("", methods =["GET"])
def read_all_customers():
    pass
    # customers = Customer.query.all()

    # customers_response = []
