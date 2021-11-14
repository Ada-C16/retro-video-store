
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
from app.helpers.customers import *
from app.models.customer import *
from app.routes.videos import Video
from app.routes.rentals import *

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

    new_customer = Customer()
    new_customer.update_attributes(request_body)
    
    db.session.add(new_customer)
    db.session.commit()

    return new_customer.customer_details(), 201

# GET /customers/<id> Gives back details about specific customer.
# Return one dictionary of customer's data.
@customers_bp.route("/<id>", methods = ["GET"])
@require_valid_id
def get_one_customer(customer):

    return customer.customer_details(), 200

# PUT /customers/<id> Updates and returns details about specific customer
# Required request body params:
#   name(str), postal_code(str), phone(str)
# Return dictionary of customer's updated data.
@customers_bp.route("<id>", methods = ["PUT"])
@require_valid_id
@require_valid_request_body
def update_customer(customer, request_body):

    customer.update_attributes(request_body)

    db.session.commit()

    return customer.customer_details(), 200

# DELETE /customer/<id> Deletes a specific customer.
# Return dictionary with customer data. "id" is the minimum required field tested for.
@customers_bp.route("<id>", methods = ["DELETE"])
@require_valid_id
def delete_customer(customer):

    db.session.delete(customer)
    db.session.commit()

    return customer.customer_details(), 200

# GET /customers/<id>/rentals 
# Gives back details about the rentals a customer has checked out
# Returns list of dictionaries with rental info

@customers_bp.route("/<id>/rentals", methods = ["GET"])
@require_valid_id
def customer_rentals(customers):
    customer = None
    # HOW DO I PASS IN THE CUSTOMER ID WHEN THE ENDPOINT IS RENTALS?
    customer_rentals = Rental.query.filter(Rental.customer_id==customer.id)

    checked_out_videos = []

    for rental in customer_rentals:
        video = Video.query.get(rental.video_id)
        response_body = {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
        }
        checked_out_videos.append(response_body)
    
    return checked_out_videos, 200