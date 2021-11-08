from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.customer import Customer

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# HELPER FUNCTIONS

# CUSTOMER ROUTES

# Get all customers
@customer_bp.route("", methods =["GET"])
def read_all_customers():
    customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(
            customers.to_dict()
        )

    return jsonify(customers_response), 200
