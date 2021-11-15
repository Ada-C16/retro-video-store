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
    name_query = request.args.get("name")
    sort_query =  request.args.get("sort")
    p_query =  request.args.get("p")
    n_query = request.args.get("n")

    if name_query:
        customers = Customer.query.filter_by(name=name_query)
        print(name_query)
    elif sort_query:
        if sort_query == "asc":
            customers = Customer.query.order_by(Customer.name.asc())
        elif sort_query == "desc":
            customers = Customer.query.order_by(Customer.name.desc())
    # if id_query:
    #     customers = Customer.query.order_by(Customer.id)
    elif n_query and p_query:
        customers = Customer.query.filter(id.between ("((n*p)-n)+1","n*p"))
    #      DBSession.query(User).filter(User.birthday.between('1985-01-17', '1988-01-17')))
    # (n+1) through (n*p) -----n=10, p = 2
    # n= 10, p = 1
    # if p = 1, and n =10, p to n
    # 1, ((10*1)-10)+1=1 to n*p
    #   ()  through (n*p)

    #    1-10  11-20  21-30  31-40


    else: 
        customers = Customer.query.order_by(Customer.id.asc()).all()
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
  