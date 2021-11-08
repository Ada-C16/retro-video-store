from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["GET"])
def get_customers():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        customers = Customer.query.order_by(Customer.name).all()
    elif sort_query == "desc":
        customers = Customer.query.order_by(Customer.name.desc()).all()
    else:
        customers = Customer.query.all()

    response_body = [Customer.to_dict() for customer in customers]
    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    response_body = {
        "customer": (customer.to_dict())
    }
    return jsonify(response_body), 200

@customers_bp.route("", methods=["POST"])
def post_new_customer():
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body\
        or "phone" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(name=request_body["name"],
    postal_code=request_body["postal_code"],
    phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    response_body = {
        "id": new_customer.id
    }
    return jsonify(response_body), 201

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer is None:
        return jsonify(None), 404

    form_data = request.get_json()
    
    if "name" not in form_data or "postal_code" not in form_data\
        or "phone" not in form_data:
        return jsonify({"details": "Invalid data"}), 400

    
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]

    db.session.commit()

    response_body = {
        "customer": (customer.to_dict())
    }
    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify(None), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({
        'id': customer.customer_id
        }), 200



# @app.errorhandler(Exception)          
# def basic_error(e):          
#     return "an error occured: " + str(e)
# https://flask.palletsprojects.com/en/2.0.x/errorhandling/