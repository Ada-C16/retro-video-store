from flask import Blueprint
from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request, abort
import datetime, requests, os
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# def valid_int(number, parameter_type):
#     try:
#         int(number)
#     except:
#        return {"message": "Invalid data"}, 400

# def get_customer_from_id(customer_id):
#     valid_int(customer_id, "customer_id")
#    #return Customer.query.get_or_404({"message":f"Customer {customer_id} was not found"}, 404 
#     return Customer.query.get_or_404(customer_id, description="{customer not found}")


# @customers_bp.route("/<customer_id>", methods=["GET"])
# def get_customer_by_id(customer_id):
#     single_customer = get_customer_from_id(customer_id)
#     return {single_customer.to_dict()}, 200

@customers_bp.route("/<id>", methods=["GET"])
def read_one_customer(id):
    try:
        int(id)
    except:
        return {"message": "Invalid data"}, 400

    customer = Customer.query.get(id)

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404        

    return customer.to_dict(), 200


@customers_bp.route("", methods=["GET"])
def get_all_cusotmers():

    customers = Customer.query.all()

    response_body = []

    if not customers:
        return jsonify([]), 200

    for customer in customers:
        response_body.append(customer.to_dict())
    
    return jsonify(response_body), 200


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    missing_data = ""
    if "name" not in request_body:
        missing_data = "name"
    elif "postal_code" not in request_body:
        missing_data = "postal_code"
    elif "phone" not in request_body:
        missing_data = "phone"
    if missing_data:
        return {"details": f"Request body must include {missing_data}."}, 400
        

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
    )
   
    db.session.add(new_customer)
    db.session.commit()
    
    return {"id": new_customer.id}, 201



@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.id}, 200


@customers_bp.route("/<customer_id>", methods=["PUT", "PATCH"])
def update_customer(customer_id):
    request_body = request.get_json()

    customer = Customer.query.get(customer_id)

    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404

    if "name" not in request_body or "phone" not in request_body \
    or "postal_code" not in request_body:
        return {"details": "Invalid request"}, 400

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    db.session.commit()
    
    return customer.to_dict(), 200