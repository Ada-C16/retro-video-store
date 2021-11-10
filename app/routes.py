from flask import abort,Blueprint,jsonify,request,make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime
import requests

from tests.test_wave_01 import CUSTOMER_ID

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    customer_response = []

    if request.method == "GET":
        customers = Customer.query.all()
        customer_response = [customers.to_dict() for customer in customers]
        return jsonify(customer_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({"details": "Invalid data"}, 400) 

        new_customer = Customer(customer_id=request_body["id"])
        db.session.add(new_customer)
        db.session.commit()
        #need to double check if CUSTOMER_ID will work
        return make_response({"id": int(CUSTOMER_ID)}, 201)

@customers_bp.route("/customers/<id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if request.method == "GET":
        if not customer:
            return make_response(f"Customer {customer_id} not found", 404)
        
        return {"customer": customer.to_dict()}

    elif request.method == "DELETE":
        if not customer:
            return make_response(f"Customer {customer_id} not found", 404)

        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": int(CUSTOMER_ID)}, 200)
##CONTINUE HERE 11/10
    elif request.method == "PUT":
        if not goal:
            return make_response("", 404)

        request_body = request.get_json()
        goal.title = request_body["title"] if "title" in request_body else goal.title

        return make_response({"goal": goal.to_dict()}, 200)