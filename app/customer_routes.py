from flask import Blueprint, jsonify, request
from app import db
from app.models.customer import Customer

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400 
    elif "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    elif "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400
    
    new_customer = Customer.from_json(request_body)
    db.session.add(new_customer)
    db.session.commit()
    return {"id": new_customer.id}, 201


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify("Customer id must be an integer"), 400

    customer = Customer.query.get(customer_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    response_body = customer.to_json()
    return (response_body, 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customer_rental(customer_id):
    if not customer_id.isnumeric():
        return jsonify("Customer id must be an integer"), 400
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify(message=f"Customer {customer_id} was not found"), 404
    videos = customer.videos
    videos_response = [video.to_json() for video in videos]
    return jsonify(videos_response), 200        


@customers_bp.route("/<customer_id>", methods=["PUT"])
def put_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify("Customer id must be an integer"), 400
    customer = Customer.query.get(customer_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    request_body = request.get_json()
    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400 
    elif "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    elif "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()
    customer = Customer.query.get(customer_id)
    return customer.to_json(), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify("Customer id must be an integer"), 400
    customer = Customer.query.get(customer_id)
    if customer is None:
        return ({"message": f"Customer {customer_id} was not found"}, 404)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.id}, 200