from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response,request, abort
from dotenv import load_dotenv
import os
from datetime import datetime
from flask import Flask


load_dotenv()
customer_bp = Blueprint("customer", __name__,url_prefix="/customers")

#Helper function
def valid_int(number):
    try:
        return int(number)     
    except:
        abort(make_response({"error": f"{number} must be an int"}, 400))

# @customer_bp.errorhandler(404)
# def resource_not_found(e):
#     return jsonify({"message":f"Customer 1 was not found"}), 404

   
# #Helper function
# def get_customer_from_id(customer_id):
#     customer_id = valid_int(customer_id)
#     return Customer.query.get_or_404(customer_id)

#Helper function
def get_object_from_id(obj, id):
    id = valid_int(id) 
    obj1 = obj.query.get(id)
    if obj1:
        return obj1
    else:       
        abort(make_response(jsonify({"message": f"{obj.__str__(obj)} {id} was not found"}), 404))

@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body:
         return {"details" : f"Request body must include name."}, 400

    if "postal_code" not in request_body:
        return {"details" : f"Request body must include postal_code."}, 400

    if "phone" not in request_body:
        return {"details" : f"Request body must include phone."}, 400

    
    new_customer = Customer(name=request_body["name"], phone=request_body["phone"],\
        postal_code=request_body["postal_code"], register_at=datetime.utcnow())
    
    db.session.add(new_customer)
    db.session.commit()
    return new_customer.to_dict(), 201

@customer_bp.route("", methods=["GET"])
def read_all_customers():
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]
    return jsonify(response)

@customer_bp.route("/<customer_id>", methods=["GET"])
def read_one_customer(customer_id):
   
        response = get_object_from_id(Customer,customer_id)
        
        return response.to_dict()

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    response = get_object_from_id(Customer, customer_id)
    request_body = request.get_json()
    if "name" not in request_body:
         return {"details" : f"Request body must include name."}, 400

    if "postal_code" not in request_body:
        return {"details" : f"Request body must include postal_code."}, 400

    if "phone" not in request_body:
        return {"details" : f"Request body must include phone."}, 400

    response.name = request_body["name"]
    print(response.name)
    response.phone = request_body["phone"]
    response.postal_code = request_body["postal_code"]
    response.register_at = datetime.utcnow()

    db.session.commit()

    return response.to_dict()

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    response = get_object_from_id(Customer, customer_id)
    
    db.session.delete(response)
    db.session.commit()
    
    return response.to_dict()
  