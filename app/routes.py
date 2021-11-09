from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from datetime import datetime
import requests
import os 

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

def make_customer_dict(customer):
 
    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone,
        "registered_at" : customer.registered_at,
        } 

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":
       
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            current_customer = make_customer_dict(customer)
            customers_response.append(current_customer)
            
        return jsonify(customers_response), 200
    # POST
    else: 
        request_body = request.get_json()
        # if post is missing postal code, name, or phone number do not post and return 400
        if "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
        elif "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        # if all required values are given in the request body, return the task info with 201
        else: 
            new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()

        return make_customer_dict(new_customer), 201

@customers_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer(id):
    try:
        int_id = int(id)
    except ValueError:
        return jsonify(""), 400

    customer = Customer.query.get(id)
    
    # Guard clause 
    if customer is None:
        return jsonify({"message": (f'Customer {id} was not found')}), 404
    
    
    if request.method == "GET": 
        return jsonify(make_customer_dict(customer)), 200
        
    elif request.method == "PUT":
        form_data = request.get_json()
        if "postal_code" not in form_data or "phone" not in form_data or "name" not in form_data:
            return jsonify(""), 400

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()
        return jsonify(make_customer_dict(customer)), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({"id": customer.id}), 200