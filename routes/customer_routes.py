from flask.helpers import make_response
from app.models.customer import Customer
from datetime import date 
from flask import Blueprint, jsonify, json, request, abort,make_response
from app import db

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")

@customer_bp.route("", methods = ["POST", "GET"])
def create_customer(): 
    if request.method is "POST":
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response("Invalid", 400)
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"]
        )
        db.session.add(new_customer)
        db.session.commit()

        return f"Customer{new_customer.id} created", 201

    elif request.method is "GET":
        customers = Customer.query.all()
        customer_response = []
        for each_customer in customers:
            customer_response.append([{
                    "id": Customer.id,
                    "name" : Customer.id,
                    "registered_at" : Customer.registered_at,
                    "postal_code" : Customer.postal_code,
                    "phone" : Customer.phone
                    }])
        return jsonify(customer_response)

@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"]) 
def handle_customers(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer is None:
        return make_response(f"Customer {customer_id} not found", 404)

    if request.method == "GET":

        return {
            "id": Customer.id,
            "name" : Customer.id,
            "registered_at" : Customer.registered_at,
            "postal_code" : Customer.postal_code,
            "phone" : Customer.phone
            }

    elif request.method == "PUT":
        request_body = request.get_json()

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return jsonify(f"Customer #{customer.id} sucessfully updated"), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify(f"Customer #{customer.id} sucessfully deleted"), 200

        