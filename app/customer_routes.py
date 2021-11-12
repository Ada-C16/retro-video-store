from flask import Blueprint, jsonify, request
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_json(customer) for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    try:
        new_customer = Customer.from_json(request_body)
        db.session.add(new_customer)
        db.session.commit()
        return {"id": new_customer.id}, 201
    except KeyError:
        if "name" not in request_body:
            return {"details": "Request body must include name."}, 400 
        elif "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if customer is None:
            return ({"message": f"Customer {customer_id} was not found"}, 404)
        # 
        response_body = customer.to_json(customer)
        return (response_body, 200)
    except:
        return ("Customer id must be an integer", 400)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customer_rental(customer_id):
    
    customer = Customer.query.get(customer_id)
    videos = customer.videos
    rental = customer.rentals
    video_list = []
    if not customer:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    elif not videos:
        return (video_list, 404)
    for video in videos:
        video_list.append(
                {
                    "release_date": video.release_date,
                    "title": video.title,
                    "due_date": rental.due_date
                        }
        )
    return video_list, 200



@customers_bp.route("/<customer_id>", methods=["PUT"])
def put_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()
        customer = Customer.query.get(customer_id)
        return customer.to_json(customer), 200
    except:
        if "name" not in request_body:
            return {"details": "Request body must include name."}, 400 
        elif "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.id}, 200



