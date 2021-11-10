
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
from app.models.customer import Customer

# Write blueprint for customer 
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


# ----------------------------------------
# ----------- CUSTOMERS ENDPOINTS --------
# ----------------------------------------

# GET /customers Lists all existing customers and details about each customer
# Successful response status: 200
# If no customers, return empty array and 200 status
# Return list of dictionaries of customer data.
@customers_bp .route("", methods = ["GET"])
def get_customers():

    customers = Customer.query.all()

    return list_of_customers(customers), 200


# POST /customers Creates a new customer with given params:
#   name (str), postal_code(str), phone(str)
# Successful response status: 201:Created
# Error status: 400: Bad request. Provide details of error if invalid input.
# Return dictionary with customer data. "id" is the minimum required field tested for.
@customers_bp .route("", methods = ["POST"])
def add_new_customer():

    request_body = request.get_json()
    
    ### Opportunity to use the invalid input decorator here if we figure out how to create one! ###
    if is_invalid(request_body):
        return is_invalid(request_body)

    new_customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()

    response_body = customer_details(new_customer), 201

    return response_body
    

# GET /customers/<id> Gives back details about specific customer.
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if customer does not exist.
# Return one dictionary of customer's data.
@customers_bp .route("/<id>", methods = ["GET"])
def get_one_customer(id):

    ### Opportunity to use the invalid id decorator here if we figure out how to create one! ###
    try:
        id = int(id)
    except ValueError:
        return {"message": "Customer id needs to be an integer"}, 400

    customer = Customer.query.get(id)
    
    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    return customer_details(customer), 200

# PUT /customers/<id> Updates and returns details about specific customer
# Required request body params:
#   name(str), postal_code(str), phone(str)
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if customer does not exist.
# Error status: 400: Bad request. Provide details of error if invalid input.
# Return dictionary of customer's updated data.
@customers_bp .route("<id>", methods = ["PUT"])
def update_customer(id):
    request_body = request.get_json()

    ### Opportunity to use the invalid id decorator here if we figure out how to create one! ###
    try:
        id = int(id)
    except ValueError:
        return {"message": "Customer id needs to be an integer"}, 400

    ### Opportunity to use the invalid input decorator here if we figure out how to create one! ###
    if is_invalid(request_body):
        return is_invalid(request_body)

    customer = Customer.query.get(id)

    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    customer.name =request_body["name"]
    customer.postal_code=request_body["postal_code"]
    customer.phone=request_body["phone"]

    db.session.commit()

    return request_body, 200

# DELETE /customer/<id> Deletes a specific customer.
# Successful response status: 200
# Error status: 404: Not found. Provide details of error if customer does not exist.
# Return dictionary with customer data. "id" is the minimum required field tested for.
@customers_bp .route("<id>", methods = ["DELETE"])
def delete_customer(id):

    try:
        id = int(id)
    except ValueError:
        return {"message": "Customer id needs to be an integer"}, 400

    customer = Customer.query.get(id)

    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404
    
    db.session.delete(customer)
    db.session.commit()

    return customer_details(customer), 200

def customer_details(customer):
    return {
    "id": customer.id,
    "name": customer.name,
    "postal_code": customer.postal_code,
    "phone": customer.phone
    } 

def list_of_customers(customers):
    return jsonify([customer_details(customer) for customer in customers])


def is_invalid(request_body):
    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    elif "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    elif "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400



## Could we write a decorator to verify input?
# def is_id_valid(wrapped_function):
#     def inner():

#     return inner