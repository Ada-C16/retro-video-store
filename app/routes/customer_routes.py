from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
import requests
from datetime import datetime, timedelta

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


# refactored and cleaned


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"],
    )
    db.session.add(new_customer)
    db.session.commit()

    response_body = {


        "id": new_customer.customer_id,
        "name": new_customer.name,
        "postal_code": new_customer.postal_code,
        "phone": new_customer.phone,

    }

    return jsonify(response_body), 201


@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_response = []

    for customer in customers:
        customer_response.append({
            "id": customer.customer_id,
            "name": customer.name,
            "registered_at": customer.registered_at,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
        })
    return jsonify(customer_response)


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):

    if customer_id.isnumeric() != True:
        return jsonify({"error": "Invalid Data"}), 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404
        # refactor with helper function
    response_body = {
        "id": customer.customer_id,
        "name": customer.name,
        "registered_at": customer.registered_at,
        "postal_code": customer.postal_code,
        "phone": customer.phone}
    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    if "name" not in request_body or type(customer.name) != str:
        return make_response("", 400)
    if "postal_code" not in request_body or type(customer.postal_code) != str:
        return make_response("", 400)
    if "phone" not in request_body or type(customer.phone) != str:
        return make_response("", 400)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.add(customer)
    db.session.commit()

    response_body = {
        "id": customer.customer_id,
        "name": customer.name,
        "registered_at": customer.registered_at,
        "postal_code": customer.postal_code,
        "phone": customer.phone,
    }

    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.customer_id}


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_rentals(customer_id):
    if customer_id.isnumeric() != True:
        return jsonify({"error": "Invalid Data"}), 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    rentals = Rental.query.filter_by(
        customer_id=customer.customer_id, videos_checked_in=False)

    response_body = list()

    for rental in rentals:
        video = Video.query.get(rental.video_id)

        response_body.append(
            {
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date})

    return jsonify(response_body), 200
