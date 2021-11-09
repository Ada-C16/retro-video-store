from app import db
from app.models.customer import Customer
from flask import Blueprint, json, jsonify, request, make_response
import datetime

customers_bp = Blueprint("customers",__name__, url_prefix="/customers")

@customers_bp.route("",methods=["GET"])

def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())

    return jsonify(customers_response),200

@customers_bp.route("/<customer_id>",methods=["GET"])
def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response(jsonify({'message': f'Customer {customer_id} was not found'}),404)
    return customer.to_dict(),200

@customers_bp.route("",methods=["POST"])
def new_customer():
    request_body = request.get_json()