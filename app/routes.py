from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime

# setup blueprints here
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers routes

# WV1 returns empty list if no customers, otherwise, list of dictionaries
# summarizing each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]
    return jsonify(response)

# WV1 adds new customer to customers. 400 error if phone, name, or 
# postal code are missing from request body. 
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

# WV1 Get data about one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer.
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        return customer.to_dict(), 200


# WV1 Update one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer, or
# if input data is invalid.
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


# WV1 Delete one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer.
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
