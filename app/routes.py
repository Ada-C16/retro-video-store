import re
from flask.blueprints import Blueprint
from app import db
from flask import Flask, jsonify, request
from .models.customer import Customer

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customer_bp.route("", methods=["GET", "POST"])
def handle_customers():
    pass

    if request.method == "POST":
        
        request_body = request.get_json()

        input_error = Customer.check_input_fields(request_body)

        if input_error:
            return input_error

        new_customer = Customer.from_json(request_body)

        db.session.add(new_customer)
        db.session.commit()

        return new_customer.to_dict(), 201
        
    elif request.method == "GET":

        customers = Customer.query.all()

        return jsonify([customer.to_dict() for customer in customers]), 200