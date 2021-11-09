from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request, abort

# Blueprint
customers_bp = Blueprint("customers_bp", __name__, url_prefix = "/customers")

# Helper Functions
def validate_int(customer_id, param_type):
    try:
        number = int(customer_id)
    except:
        abort(make_response({"message": f"{param_type} needs to be an integer."}, 400))

def get_customer_data_with_id(customer_id):
    validate_int(customer_id, "id")
    # return Customer.query.get_or_404(customer_id, description={"message": f"Customer {customer_id} was not found"})
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

    return customer

# Routes
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customer_data = []

    customers = Customer.query.all()
    for customer in customers:
        customer_data.append(customer.to_dict())

    return jsonify(customer_data)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if request_body == None:
        return make_response("You much include name, phone and postcode in order to add customer data."), 404

    if "name" not in request_body or "phone" not in request_body or "postcode" not in request_body:
        return make_response("You much include name, phone and postcode in order to add customer data."), 404

    new_customer = Customer(
        name = request_body["name"],
        phone = request_body["phone"],
        postal_code = request_body["postal_code"]
    )
    
    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = get_customer_data_with_id(customer_id)

    return jsonify(customer.to_dict())

# @customers_bp.route("/<customer_id>", methods=["PUT"])
# def update_one_customer(customer_id):
#     request_body = request.get_json()
#     customer = get_customer_data_with_id(customer_id)

#     if customer == None:
#         error_message = {}
#         error_message["message"] = f"Customer {customer_id} was not found"
#         return error_message, 404

#     return jsonify(customer.to_dict())