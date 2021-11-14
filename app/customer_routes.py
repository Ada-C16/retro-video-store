from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request
from app.models.video import Video
from datetime import datetime
import requests
import os

customer_bp = Blueprint("customers", __name__, url_prefix=("/customers"))


@customer_bp.route("", methods=["GET"])
def get_customer():
    if request.method == "GET":
        customers = Customer.query.all()
        customer_response = []
        for customer in customers:
            customer_response.append(
                {
                    "id": customer.customer_id,
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

        if "title" not in request_body:

            return jsonify({"details": "Invalid data"}), 400
        else:

            new_goal = Customer(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()


@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def gpd_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return (
            jsonify({"message": f"Customer {customer_id} was not found"}),
            404,
        )

    if request.method == "GET":

        customer_response = {
            "id": customer.customer_id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
        }

        return jsonify(customer_response), 200

    if request.method == "PUT":
        # form.data = request.get_json()
        pass

    return jsonify(
        "/customers/1",
        {
            "name": f"Updated ${CUSTOMER_NAME}",
            "phone": f"Updated ${CUSTOMER_PHONE}",
            "postal_code": f"Updated ${CUSTOMER_POSTAL_CODE}",
        },
    )


@customer_bp.route("/hello", methods=["GET"])
def get_hello():
    return jsonify(None), 400
