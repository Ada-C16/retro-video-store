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
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]
    return jsonify(response)

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def post_customers():
    response_body = request.get_json()
    if not Customer.is_data_valid(response_body)[0]:
        return Customer.is_data_valid(response_body)[1], 400
    else:
        new_customer = Customer.from_json(response_body)
    
    db.session.add(new_customer)
    db.session.commit()
    return {"id": new_customer.customer_id}, 201

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        return customer.to_dict(), 200

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        response_body = request.get_json()
    if not Customer.is_data_valid(response_body)[0]:
        return Customer.is_data_valid(response_body)[1], 400
    customer.name = response_body["name"]
    customer.postal_code = response_body["postal_code"]
    customer.phone = response_body["phone"]
    db.session.commit()
    return customer.to_dict(), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        db.session.delete(customer)
        db.session.commit()
        return {"id": customer.customer_id}, 200
