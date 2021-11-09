from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request
from datetime import datetime

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["POST"])
def customer_create():
    request_body = request.get_json()

    # is the registered_at not required?
    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(
        name=request_body["name"],
        phone=request_body["phone"],
        postal_code=request_body["postal_code"],
        registered_at=request_body["registered_at"]
    )
    db.session.add(new_customer)
    db.session.commit()

    # response_body = {new_customer.customer_dict()}
    # return jsonify(response_body), 201
    return jsonify({"id": new_customer.customer_id})


@customers_bp.route("", methods=["GET"])
def handle_customers():
    customers = Customer.query.all()
    response_body = []
    # for customer in customers:
    #     response_body.append({customers.customer_dict()})
    for customer in customers:
        response_body.append({
            "id": customers.customer_id,
            "name": customers.name,
            # "registered_at": customers.registered_at,
            "postal_code": customers.postal_code,
            "phone": customers.phone
})

    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def customer_get(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify("Not Found", 404)

    return jsonify(customer.customer_dict), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def customer_put(customer_id):
    customer = Customer.query.get(customer_id)

    if customer == None:
        return jsonify("Not Found", 404)

    request_body = request.get_json()

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]
    # is registered not required?
    response_body = {customer.customer_dict}

    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = Customer.query.get(customer_id)

    if customer == None:
        return jsonify("Not Found", 404)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.customer_id})