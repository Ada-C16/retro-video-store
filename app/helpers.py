from functools import wraps
from .models.customer import Customer
from flask import jsonify

# decorator to check if id is valid

# decorator to check if response body is valid

def require_valid_id(endpoint):
    @wraps(endpoint)
    def fn(*args, id, **kwargs):
        try:
            id = int(id)
        except ValueError:
            return {"message": "Customer id needs to be an integer"}, 400

        customer = Customer.query.get(id)

        if not customer: 
            return {"message": f"Customer {id} was not found"}, 404

        return endpoint(*args, customer=customer, **kwargs)
    return fn

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
