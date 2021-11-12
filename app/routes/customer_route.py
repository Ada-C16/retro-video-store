from flask import Blueprint, jsonify
from app import db 
from app.models.customer import Customer 
from app.models.rental import Rental
from datetime import datetime
from .helpers import id_is_valid, request_has_all_required_categories

customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def customers():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("", methods=["POST"])
def add_customer():
    request_data, error_msg = request_has_all_required_categories("customer")
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
    
    return jsonify(new_customer.to_json()), 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def customer(customer_id):
    customer, error_msg = id_is_valid(customer_id, "customer")
    if error_msg is not None:
        return error_msg 

    return jsonify(customer.to_json()), 200

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer, error_msg = id_is_valid(customer_id, "customer")
    if error_msg is not None:
        return error_msg 

    request_data, error_msg = request_has_all_required_categories("customer")
    if error_msg is not None:
        return error_msg

    customer.name = request_data["name"]
    customer.phone = request_data["phone"]
    customer.postal_code = request_data["postal_code"]
    db.session.commit()

    return jsonify(customer.to_json()), 200 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer, error_msg = id_is_valid(customer_id, "customer")
    if error_msg is not None:
        return error_msg 
    
    db.session.delete(customer)
    db.session.commit()

    return jsonify({ "id": int(customer_id) }), 200 

@customers_bp.route("<customer_id>/rentals", methods=["GET"])
def customer_rentals(customer_id):
    _, error_msg = id_is_valid(customer_id, "customer")
    if error_msg is not None:
        return error_msg  
        
    rentals = Rental.query.filter_by(customer_id=int(customer_id))

    video_details_response = []
    for rental_object in rentals:
        video_details_response.append(rental_object.video_details())

    return jsonify(video_details_response), 200
