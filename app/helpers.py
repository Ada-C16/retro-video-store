from functools import wraps
from .models.customer import Customer

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

