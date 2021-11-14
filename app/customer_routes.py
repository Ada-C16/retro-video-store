from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
import datetime

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    for customer in customers:
        if customer.deleted_at is not None:
            customers.remove(customer)
    customer_response = [customer.customer_dict() for customer in customers]
    return jsonify(customer_response), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customers_by_id(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)
    if not customer:
        response_body = {"message": f"Customer {customer_id} was not found"}
        return jsonify(response_body), 404
    if customer.deleted_at is not None:
        return jsonify(None), 404
    response_body = customer.customer_dict()
    return jsonify(response_body), 200


@customers_bp.route("", methods=["POST"])
def post_customer():
    request_body = request.get_json()
    if "name" not in request_body:
        response_body = {"details": "Request body must include name."}
        return jsonify(response_body), 400
    elif "postal_code" not in request_body:
        response_body = {"details": "Request body must include postal_code."}
        return jsonify(response_body), 400
    elif "phone" not in request_body:
        response_body = {
            "details": "Request body must include phone."}
        return jsonify(response_body), 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
    )
    db.session.add(new_customer)
    db.session.commit()
    response_body = new_customer.customer_dict()
    return jsonify(response_body), 201


@customers_bp.route("/<customer_id>", methods=["PUT"])
def put_customer_by_id(customer_id):

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    request_body = request.get_json()
    if (
        "name" not in request_body or
        "postal_code" not in request_body or
        "phone" not in request_body
    ):
        return jsonify({"details": "Invalid data"}), 400

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    response_body = customer.customer_dict()
    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    customer.deleted_at = datetime.datetime.now()

    db.session.commit()

    response_body = customer.customer_dict()
    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def rentals_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        response_body = {"message": f"Customer {customer_id} was not found"}
        return jsonify(response_body), 404

    rental_response = [rental.id for rental in customer.rentals]
    if not rental_response:
        return jsonify([]), 200

    response_body = [Video.query.get(video).create_dict()
                     for video in rental_response]
    return jsonify(response_body), 200
