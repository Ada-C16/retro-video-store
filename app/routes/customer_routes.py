from app import db
from app.models.customer import Customer
from flask import Blueprint, request, jsonify
from datetime import datetime
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    response_body = [customer.to_dict() for customer in customers]
    return jsonify(response_body)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    if "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    new_customer = Customer(
        name= request_body["name"],
        phone= request_body["phone"],
        postal_code= request_body["postal_code"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return new_customer.to_dict(), 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
    except:
        return jsonify(None), 400

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    return customer.to_dict()

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return customer.to_dict()

# @customers_bp.route("/<customer_id>", methods=["PUT"])
# def update_customer(customer_id):
#     customer = Customer.query.get(customer_id)
#     request_body = request.get_json()

#     customer.name = request_body["name"]
#     customer.phone = request_body["phone"]
#     customer.postal_code = request_body["postal_code"]

#     db.session.commit()

#     return customer.to_dict()



