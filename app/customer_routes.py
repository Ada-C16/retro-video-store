import re
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
import requests, os, datetime
from datetime import timedelta

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# creates a customer
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_data = request.get_json()

    validate_input(request_data)

    new_customer = Customer(
        name = request_data["name"],
        postal_code = request_data["postal_code"],
        phone = request_data["phone"]
    )

    new_customer.registered_at = datetime.datetime.now()

    db.session.add(new_customer)
    db.session.commit()

    return make_response(
        new_customer.to_dict(), 201
    )

# lists all existing customers and details about each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []
    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# gets details about a specific customer
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    customer = validate_id(customer_id)

    return make_response(
        customer.to_dict(), 200
    )

# updates and return details about a specific customer
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = validate_id(customer_id)

    request_data = request.get_json()

    validate_input(request_data)

    customer.name = request_data["name"]
    customer.postal_code = request_data["postal_code"]
    customer.phone = request_data["phone"]

    db.session.commit()

    return make_response(
        customer.to_dict(), 200
    )
    
# deletes a specific customer
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = validate_id(customer_id)
    
    if customer.rentals:
        for this_cust in customer.rentals:
            db.session.delete(this_cust)
            db.session.commit()
        return make_response("",200)
    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.id}, 200

# lists the videos a customer currently has checked out
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def videos_checked_out_by_customer(customer_id):
    customer = validate_id(customer_id)

    videos_checked_out = []

    rentals = customer.rentals
    for rental in rentals:
        videos_checked_out.append(
            {
                "title": rental.video.title,
                "release_date": rental.video.release_date,
                "due_date": rental.due_date
            }
        )

    return jsonify(videos_checked_out), 200

# ************************************************* ENHANCEMENTS ************************************************

# lists the videos a customer has checked out in the past
@customers_bp.route("/<customer_id>/history", methods=["GET"], strict_slashes=False)
def get_customer_history(customer_id):
    customer = validate_id(customer_id)

    customer_history=[]

    for cust in customer.rentals:
        customer_history.append(
            {
                "title": cust.video.title,
                "checkout_date": cust.due_date-timedelta(days=7),
                "due_date": cust.due_date
            }
        )

    return jsonify(customer_history), 200

# ********************************************** HELPER FUNCTIONS ***********************************************
def validate_id(id):
    try:
        id = int(id)
    except:
        abort(400, {"error": f"{id} must be numeric"})

    customer = Customer.query.get(id)
    if not customer:
        abort(make_response({"message":f"Customer {id} was not found"}, 404))
    return customer

def validate_input(input):
    if "name" not in input:
        abort(make_response(
            {"details": f"Request body must include name."}, 400
        ))
    
    if "postal_code" not in input:
        abort(make_response(
            {"details": f"Request body must include postal_code."}, 400
        ))

    if "phone" not in input:
        abort(make_response(
            {"details": f"Request body must include phone."}, 400
        ))