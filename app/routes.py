from flask import Blueprint, jsonify, request, make_response
from app.models.customer import Customer
from app import db
import requests
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers Routes

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)