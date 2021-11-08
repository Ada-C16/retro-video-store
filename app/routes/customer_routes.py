from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request

# Blueprint
customers_bp = Blueprint("customers_bp", __name__, url_prefix = "/customers")

# Helper Functions
def get_customer_data_with_id(customer_id):
    return Customer.get_or_404(customer_id, descriptions={"details": "Invalid data"})

# Routes
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customer_data = []

    customers = Customer.query.all()
    for customer in customers:
        customer_data.append(customer.to_dict())

    return jsonify(customer_data)

@customers_bp.route("", methods=["POST"])
def add_customer():
    request_body = request.get_json()

    if request_body == None:
        return make_response("You much include name, phone and postcode in order to add customer data."), 404

    if "name" not in request_body or "phone" not in request_body or "postcode" not in request_body:
        return make_response("You much include name, phone and postcode in order to add customer data."), 404

    new_customer = Customer(
        name = request_body["name"],
        phone = request_body["phone"],
        post_code = request_body["post_code"]
    )
    
    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer), 200