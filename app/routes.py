from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    response = []
    for customer in customers:
        response.append(customer.to_dict())

    return jsonify(response), 200


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer.from_dict(request_body)
        db.session.add(new_customer)
        db.session.commit()

        response = {
            "id" : new_customer.customer_id,
            "message" : "Customer successfully created."
        }

        return jsonify(response), 201
    
    except KeyError:
        if "postal_code" not in request_body.keys():
            response = {
                "details" : "Request body must include postal_code."
            }
        elif "name" not in request_body.keys():
            response = {
                "details" : "Request body must include name."
            }
        elif "phone" not in request_body.keys():
            response = {
                "details" : "Request body must include phone."
            }
        
        return jsonify(response), 400

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_a_customer(customer_id):
    if type(customer_id) != int:
        return jsonify(None), 400
    else:
        customer = Customer.query.get(customer_id)
        if not customer: 
            return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        else:
            return jsonify(customer.to_dict()), 200


    

    # if type(customer_id) == int:
        
    # else:
    #     return jsonify(None), 400

   

    
    
    
        
