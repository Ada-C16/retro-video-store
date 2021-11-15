from app import db
from app.models.customer import Customer
from flask import Blueprint, json, jsonify, request
from app.models.video import Video
from datetime import datetime
import requests
import os

from tests.test_wave_01 import CUSTOMER_NAME

customer_bp = Blueprint("customers", __name__, url_prefix=("/customers"))


@customer_bp.route("", methods=["GET"])
def get_customer():
    if request.method == "GET":
        customers = Customer.query.all()
        customer_response = []
        for customer in customers:
            customer_response.append(
                {
                    "id": customer.id,
                    "name": customer.name,
                    "postal_code": customer.postal_code,
                    "phone": customer.phone,
                }
            )
    return jsonify(customer_response), 200


@customer_bp.route("", methods=["POST"])
def put_customer():
    if request.method == "POST":
        request_body = request.get_json()

        if "name" not in request_body:
            return jsonify({"details": "Request body must include name."}), 400

        if "postal_code" not in request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400

        if "phone" not in request_body:
            return jsonify({"details": "Request body must include phone."}), 400

        else:

            new_customer = Customer(
                name=request_body["name"],
                phone=request_body["phone"],
                postal_code=request_body["postal_code"],
            )

            db.session.add(new_customer)
            db.session.commit()

            return jsonify(new_customer.customer_information()), 201


@customer_bp.route("/<customer_id>", methods=["GET", "PUT"])
def gpd_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return (
            jsonify({"message": f"Customer {customer_id} was not found"}),
            404,
        )

    if request.method == "GET":

        customer_response = {
            "id": customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
        }

        return jsonify(customer_response), 200

    if request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body:
            return jsonify(None), 400
        if "postal_code" not in request_body:
            return jsonify(None), 400
        else:
            form_data = request.get_json(customer_id)
            customer.name = form_data["name"]
            customer.phone = form_data["phone"]
            customer.postal_code = form_data["postal_code"]

            db.session.commit()

            return jsonify(customer.customer_information()), 200


@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer == None:
        return jsonify(message=f"Customer {customer_id} was not found"), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify(id=customer.id), 200


@customer_bp.route("/hello", methods=["GET"])
def get_hello():
    return jsonify(None), 400


@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customers_current_rentals(customer_id):
    pass
