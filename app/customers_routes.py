from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request
from datetime import datetime

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["POST"])
def customer_create():
    request_body = request.get_json()
    
    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body or "registered_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(
        name=request_body["name"],
        phone=request_body["phone"],
        postal_code=request_body["postal_code"],
        registered_at=request_body["registered_at"]
    )
    db.session.add(new_customer)
    db.session.commit()

    response_body = {new_customer.customer_dict()}
    return jsonify(response_body), 201
