from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime

# setup blueprints here
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# Customers routes

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]
    return jsonify(response)

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def post_customers():
    response_body = request.get_json()
    if not Customer.is_data_valid(response_body):
        return {"details": "invalid data"}, 404
    else:
        new_customer = Customer.from_json(response_body)
    
    db.session.add(new_customer)
    db.session.commit()
    return {"id": new_customer.customer_id}, 201

