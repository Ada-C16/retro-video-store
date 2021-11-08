import datetime, requests, os
from app import db
from app.models.customer import Customer
# from app.models.video import Video
from flask import Blueprint, jsonify, make_response, request
from dotenv import load_dotenv

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# creates a customer
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(
        new_customer.to_dict(), 201
    )

# lists all existing customers and details about each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []
    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# gets details about a specific customer
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400
        
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    return make_response(
        customer.to_dict(), 200
    )

# updates and return details about a specific customer
# NOT PASSING
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return jsonify({
        "name": f"Updated ${customer.name}",
        "phone": f"Updated ${customer.phone}",
        "postal_code": f"Updated ${customer.postal_code}"
        }        
    )
    

# deletes a specific customer
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    db.session.delete(customer)
    db.session.commit()

    return make_response(
        {"id": customer.id}, 200
    )

    # return {"id": customer.id}, 200