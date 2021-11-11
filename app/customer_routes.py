from app import db
from app.models.customer import Customer, find_customer
from app.models.rental import *
from app.video_routes import build_videos_response
from flask import Blueprint, request, make_response, jsonify
import os 

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("", methods = ["GET"])
def get_customers():
    sort_query = request.args.get("sort")
    name_query = request.args.get("name")
    phone_query = request.args.get("phone")
    if sort_query:
        customers = Customer.query.order_by(eval(sort_query)(Customer.name))
    elif name_query:
        customers = Customer.query.filter(Customer.name.ilike(('%'+name_query+'%')))
    elif phone_query:
        customers = Customer.query.filter(Customer.phone.ilike(('%'+phone_query+'%')))
    else:
        customers = Customer.query.all() 
    customers_response = [Customer.return_customer_info(customer) for customer in customers]
    return make_response(jsonify(customers_response), 200)


@customer_bp.route("/<id>/rentals", methods = ["GET"])
def get_customer_rentals(id):
    customer = find_customer(id)
    if not customer["found"]:
        return customer["return"]
    videos = query_customers_videos(customer["info"].id)
    video_info = build_videos_response(videos)
    return make_response(jsonify(video_info), 200)


@customer_bp.route("", methods = ["POST"])
def post_customer():
    from datetime import datetime
    request_body = request.get_json()
    try:
        name = request_body["name"]
    except:
        return make_response({"details": "Request body must include name."}, 400)
    try:     
        phone = request_body["phone"]
    except:
        return make_response({"details": "Request body must include phone."}, 400)
    try:    
        postal_code = request_body["postal_code"]
    except:
        return make_response({"details": "Request body must include postal_code."}, 400)

    new_customer = Customer(
        name = name,
        phone = phone, 
        postal_code = postal_code,
        registered_at = datetime.now()
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(Customer.new_customer(new_customer), 201)


@customer_bp.route("/<id>", methods = ["GET"])
def get_customer(id):
    customer = find_customer(id)
    if customer["found"]:
        return make_response(Customer.return_customer_info(customer["info"]), 200)
    return customer["return"]


@customer_bp.route("/<id>", methods = ["PUT"])
def put_customer(id):
    customer = find_customer(id)
    
    if not customer["found"]:
        return customer["return"]
    
    request_body = request.get_json()
    
    try:
        customer["info"].name = request_body["name"]
        customer["info"].phone = request_body["phone"]
        customer["info"].postal_code = request_body["postal_code"]

    except:
            return make_response("", 400)
    
    db.session.commit()

    return make_response(Customer.update_customer(customer["info"]), 200)



@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):
    customer = find_customer(id)
    if not customer["found"]:
        return customer["return"]
    db.session.delete(customer["info"])
    db.session.commit()

    return make_response({"id": int(id)}, 200)