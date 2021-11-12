from functools import wraps
from app.models.customer import Customer
from flask import jsonify, request


# decorator to check if response body is valid

# Decorator to check if id is an integer and if the customer exists.

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

# Decorator to check if the request_body includes name, postal_code, and phone.
def require_valid_request_body(endpoint):
    @wraps(endpoint)
    def fn(*args, **kwargs):
        request_body = request.get_json()

        if "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        elif "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
        else:
            return endpoint(*args, request_body=request_body, **kwargs)
    return fn

def list_of_customers(customers):
    return jsonify([customer.customer_details() for customer in customers])
