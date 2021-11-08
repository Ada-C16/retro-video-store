from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request

# Blueprint
customers_bp = Blueprint("customers_bp", __name__, url_prefix = "/customers_bp")

# Helper Functions
def get_customer_data_with_id(customer_id):
    return Customer.get_or_404(customer_id, descriptions={"details": "Invalid data"})

# Routes
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customer_data = []

    customers = Customer.query.all()

    for customer in customers:
        customer_data.append(customer.to_dict())

    return customer_data

