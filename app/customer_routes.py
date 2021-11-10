from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request
from datetime import datetime

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["POST"])
def customer_create():
    request_body = request.get_json()

    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        response_body ={}
        if "name" not in request_body:
            response_body["details"] = "Request body must include name."
        elif "phone" not in request_body:
            response_body["details"] = "Request body must include phone."
        elif "postal_code" not in request_body:
            response_body["details"] = "Request body must include postal_code."
        return jsonify(response_body), 400
    
    new_customer = Customer(
        name=request_body["name"],
        phone=request_body["phone"],
        postal_code=request_body["postal_code"],

    )
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.customer_id}), 201


@customers_bp.route("", methods=["GET"])
def handle_customers():
    customers = Customer.query.all()
    response_body = []
    for customer in customers:
        response_body.append(customer.customer_dict())

    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def customer_get(customer_id):
    try:
        customer = Customer.query.get(customer_id)
    except:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 400
            
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        

    return jsonify(customer.customer_dict()), 200

# WORK IN PROGRESS
@customers_bp.route("/<customer_id>", methods=["PUT"])
def customer_put(customer_id):
    # customer = Customer.query.get(customer_id)
    try:
        customer = Customer.query.get(customer_id)
    except:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 400

    if customer == None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    request_body = request.get_json()

    if "name" in request_body:
        customer.name = request_body["name"]
    if "phone" in request_body:
        customer.phone = request_body["phone"]
    if "postal_code" in request_body:
        customer.postal_code = request_body["postal_code"]

    if "name" in request_body or "phone" in request_body or "postal_code" in request_body:
        response_body ={}
        response_body["name"] = customer.name
        response_body["phone"] = customer.phone 
        response_body["postal_code"] = customer.postal_code 

    # db.session.commit()
    try:
        db.session.commit()
    except:
        return jsonify("Invalid"), 400

    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = Customer.query.get(customer_id)

    if customer == None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.customer_id}), 200