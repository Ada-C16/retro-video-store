from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from dotenv import load_dotenv
load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]

    return jsonify(response), 200


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer.from_dict(request_body)
        db.session.add(new_customer)
        db.session.commit()

        response = {
            "id": new_customer.customer_id,
            "message": "Customer successfully created."
        }

        return jsonify(response), 201

    except KeyError:
        if "postal_code" not in request_body.keys():
            response = {
                "details": "Request body must include postal_code."
            }
        elif "name" not in request_body.keys():
            response = {
                "details": "Request body must include name."
            }
        elif "phone" not in request_body.keys():
            response = {
                "details": "Request body must include phone."
            }

        return jsonify(response), 400


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_a_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    return jsonify(customer.to_dict()), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.phone = request_body["phone"]
        customer.postal_code = request_body["postal_code"]

        db.session.commit()

        return jsonify(customer.to_dict()), 200

    except KeyError:
        if "postal_code" not in request_body.keys():
            response = {
                "details": "Request body must include postal_code."
            }
        elif "name" not in request_body.keys():
            response = {
                "details": "Request body must include name."
            }
        elif "phone" not in request_body.keys():
            response = {
                "details": "Request body must include phone."
            }

        return jsonify(response), 400


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    response = {
        "id": customer.customer_id,
        "message": "Customer successfully deleted."
    }

    return jsonify(response), 200


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    response_body = [video.to_dict() for video in customer.videos]

    return jsonify(response_body), 200
