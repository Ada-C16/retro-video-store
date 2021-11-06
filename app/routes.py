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
    if "name" not in request_body:
        return jsonify({ "details" : "Request body must include name." }), 400
    if "postal_code" not in request_body:
        return jsonify({ "details" : "Request body must include postal_code." }), 400 
    if "phone" not in request_body:
        return jsonify({ "details" : "Request body must include phone." }), 400 
    
    new_customer = Customer(
        name=request_body["name"], 
        postal_code=request_body["postal_code"],
        phone=request_body["phone"],
        register_at = datetime.now()
    )
    
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({ "customer" : new_customer.to_json() }), 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def customer(customer_id):
    if not customer_id.isnumeric():
        return "", 400 
    
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404 

    return jsonify(customer.to_json()), 200

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    request_data = request.get_json()
    for required_category in ["name", "phone", "postal_code"]:
        if required_category not in request_data: 
            return "", 400 

    customer.name = request_data["name"]
    customer.phone = request_data["phone"]
    customer.postal_code = request_data["postal_code"]
    db.session.commit()

    return jsonify(customer.to_json()), 200 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404 
    
    db.session.delete(customer)
    db.session.commit()

    return jsonify({ "id": int(customer_id) }), 200 
