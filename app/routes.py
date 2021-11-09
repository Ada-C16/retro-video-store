from app import db
from flask import Blueprint
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------

# GET CUSTOMERS ALL

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    
    for customer in customers:
        customers_response.append(customer.to_json())
    #     customers_response.append({
    #     "id": customer.id,
    #     "name": customer.name,
    #     "registered_at": customer.registered_at, 
    #     "postal_code": customer.postal_code, 
    #     "phone": customer.phone})
    return jsonify(customers_response), 200





# GET CUSTOMER BY ID
@customers_bp.route("/<id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
    
    # elif customer.id.isalpha() == True:
    #     return 400
    
    else:
        jsonify(customer.to_json()), 200
        
        # jsonify(
        #     {"id": customer.id,
        #      "name": customer.name,
        #      "registered_at": customer.registered_at,"postal_code": customer.postal_code,
        #      "phone": customer.phone}), 200



# POST CUSTOMER
@customers_bp.route("", methods=["POST"])
def create_customer():
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
        phone = request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
        
    return jsonify({"id": new_customer.id}), 201



# PUT CUSTOMER
@customers_bp.route("/<id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
        
    request_body = request.get_json()
    customer.name=request_body["name"] 
    customer.postal_code=request_body["postal_code"] 
    customer.phone=request_body["phone"] 
    
    db.session.commit()
    return jsonify(customer.to_json()), 200
    # return jsonify({
    # "name": customer.name,
    # "postal_code": customer.postal_code,
    # "phone": customer.phone}), 200


# DELETE CUSTOMER
@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
    else:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.id}), 200