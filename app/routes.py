from flask import Blueprint, jsonify, request
from app import db 
from app.models.customer import Customer 
from datetime import datetime

customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

CUSTOMER_REQUIRED_CATEGORIES = ["name", "phone", "postal_code"]

# helper methods for validation 
def customer_id_is_valid(customer_id):
    '''
    returns two values: a customer object or "invalid", and an error message; 
    if no error is present, the error message is None
    '''
    if not customer_id.isnumeric():
        return "invalid", ("", 400)
    
    customer = Customer.query.get(customer_id)
    if not customer:
        return "invalid", ({"message": 
                            f"Customer {customer_id} was not found"}, 
                            404)  

    # no error was caught; the customer_id is valid 
    return customer, None 

def request_has_all_required_categories():
    '''
    returns two values: request data in json format, and an error message;
    if no error is present, the error message is None 
    '''
    request_data = request.get_json()
    for required_category in CUSTOMER_REQUIRED_CATEGORIES:
        if required_category not in request_data: 
            return request_data, (jsonify({ 
                    "details" : 
                    f"Request body must include {required_category}." }
                ), 400)

    # no error was caught; all required categories are present 
    return request_data, None  

@customers_bp.route("", methods=["GET"])
def customers():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("", methods=["POST"])
def add_customer():
    request_data, error_msg = request_has_all_required_categories()
    if error_msg is not None:
        return error_msg
    
    new_customer = Customer(
        name=request_data["name"], 
        postal_code=request_data["postal_code"],
        phone=request_data["phone"],
        register_at = datetime.now()
    )
    
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({ "customer" : new_customer.to_json() }), 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def customer(customer_id):
    customer, error_msg = customer_id_is_valid(customer_id)
    if error_msg is not None:
        return error_msg 
        
    return jsonify(customer.to_json()), 200

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer, error_msg = customer_id_is_valid(customer_id)
    if error_msg is not None:
        return error_msg 

    request_data, error_msg = request_has_all_required_categories()
    if error_msg is not None:
        return error_msg

    customer.name = request_data["name"]
    customer.phone = request_data["phone"]
    customer.postal_code = request_data["postal_code"]
    db.session.commit()

    return jsonify(customer.to_json()), 200 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer, error_msg = customer_id_is_valid(customer_id)
    if error_msg is not None:
        return error_msg 
    
    db.session.delete(customer)
    db.session.commit()

    return jsonify({ "id": int(customer_id) }), 200 
