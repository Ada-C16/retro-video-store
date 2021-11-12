
# ---------------------------------------
# ----------- CUSTOMERS SETUP -----------
# ---------------------------------------

## IN OTHER DOCS ##

# Set up the customer model -> DONE
# Set up app.__init__.py (register blueprint)--> DONE

## IN THIS DOC ##

# Import necessary packages
from flask import Blueprint, json, jsonify, request, make_response
from flask_sqlalchemy import _make_table
from app import db
from app.helpers import *
from app.models.customer import *

# Write blueprint for customer 
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


# ----------------------------------------
# ----------- CUSTOMERS ENDPOINTS --------
# ----------------------------------------

# GET /customers Lists all existing customers and details about each customer.
# Return list of dictionaries of customer data. Return empty array if no customers.
@customers_bp.route("", methods = ["GET"])
def get_customers():

    customers = Customer.query.all()

    return list_of_customers(customers), 200

# POST /customers Creates a new customer with given params:
#   name (str), postal_code(str), phone(str)
# Return dictionary with customer data. "id" is the minimum required field tested for.
@customers_bp.route("", methods = ["POST"])
@require_valid_request_body
def add_new_customer(request_body):

    new_customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()

    response_body = new_customer.customer_details(), 201

    return response_body
    

# GET /customers/<id> Gives back details about specific customer.
# Return one dictionary of customer's data.
@customers_bp.route("/<id>", methods = ["GET"])
@require_valid_id
def get_one_customer(customer):

    response_body = customer.customer_details(), 200
    return response_body

# PUT /customers/<id> Updates and returns details about specific customer
# Required request body params:
#   name(str), postal_code(str), phone(str)
# Return dictionary of customer's updated data.
@customers_bp.route("<id>", methods = ["PUT"])
@require_valid_id
@require_valid_request_body
def update_customer(customer, request_body):

    customer.name =request_body["name"]
    customer.postal_code=request_body["postal_code"]
    customer.phone=request_body["phone"]

    db.session.commit()

    return request_body, 200

# DELETE /customer/<id> Deletes a specific customer.
# Return dictionary with customer data. "id" is the minimum required field tested for.
@customers_bp.route("<id>", methods = ["DELETE"])
@require_valid_id
def delete_customer(customer):

    db.session.delete(customer)
    db.session.commit()

    response_body = customer.customer_details(), 200

    return response_body


