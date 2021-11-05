from flask import Blueprint, jsonify, make_response, request
from app import db 
from app.models.customer import Customer 
from datetime import datetime

customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def customers():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("", methods=["POST"])
def add_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or\
        "phone_number" not in request_body:
        return { "Details" : "Invalid data" }, 400 
    
    new_customer = Customer(
        name=request_body["name"], 
        postal_code=request_body["postal_code"],
        phone_number=request_body["phone_number"],
        register_at = datetime.now()
    )
    
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({ "customer" : new_customer.to_json() }), 201

