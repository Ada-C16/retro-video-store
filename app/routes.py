from flask import Blueprint, jsonify, request, abort, make_response
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import date
import requests, os
from dotenv import load_dotenv

video_bp = Blueprint('video', __name__, url_prefix="/videos")
customer_bp = Blueprint('customer', __name__, url_prefix="/customers")
load_dotenv()

@customer_bp.route("", methods=["POST", "GET"])
def handle_customers():
    if request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body:
            return jsonify({"details": "Request body must include name."}), 400 
        elif "postal_code" not in request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400
        elif "phone" not in request_body:
            return jsonify({"details": "Request body must include phone."}), 400
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"]
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_dict()), 201

    elif request.method == "GET":
        customers=Customer.query.all()
        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_dict())
        return jsonify(customers_response), 200
        


@customer_bp.route("/<customer_id>", methods= ["GET", "PUT", "DELETE"])
def handle_customer(customer_id):
    
    try:
        customer_id = int(customer_id)
    except ValueError:
            return jsonify({"Error": "Customer ID must be an integer."}), 400
    customer = Customer.query.get(customer_id)        
    if customer is None:
        return make_response({"message": f"Customer {customer_id} was not found"}), 404
    
    elif request.method == "GET":
        
        customer= Customer.query.get(customer_id)
        if customer is None:
            return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        return jsonify(customer.to_dict()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
            return jsonify({"details": "Request body must include name, phone, and postal code."}), 400
        customer.name=request_body["name"]
        customer.phone=request_body["phone"]
        customer.postal_code=request_body["postal_code"]
        db.session.commit()
        
        return jsonify(customer.to_dict()), 200
    elif request.method == "DELETE":
        customer_id=int(customer_id)
        customer=Customer.query.get(customer_id)
        db.session.delete(customer)
        db.session.commit()

        return({"id":customer_id}), 200