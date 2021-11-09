from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, request
import requests
from datetime import datetime
import os
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")



# create
@customers_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "name" not in request_body: 
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:  
        return jsonify({"details": "Request body must include postal_code."}) , 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400 
    
    # elif "register_at" not in request_body:
    #     return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(
                    name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"],
                    )
    db.session.add(new_customer)
    db.session.commit()

    response_body = {
       
            
            "id": new_customer.customer_id,
            "name": new_customer.name,
            "postal_code": new_customer.postal_code,
            "phone": new_customer.phone,
            
        }
    
    return jsonify(response_body), 201
