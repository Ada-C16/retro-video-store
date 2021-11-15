from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, request, jsonify

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    response_body = [customer.to_dict() for customer in customers]
    return jsonify(response_body)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    error_message = validate_request(request_body)
    if error_message:
        return error_message

    new_customer = Customer(
        name= request_body["name"],
        phone= request_body["phone"],
        postal_code= request_body["postal_code"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return new_customer.to_dict(), 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
    except:
        return jsonify(None), 400

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    return customer.to_dict()

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return customer.to_dict()

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    error_message = validate_request(request_body)
    if error_message:
        return error_message

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    db.session.commit()

    return customer.to_dict()

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404

    videos= []
    for video in customer.videos:
        rental = Rental.query.filter_by(customer_id = customer.id, video_id = video.id).first()
        video = video.to_dict_using_rentals()
        video["due_date"] = rental.due_date
        videos.append(video)

    return jsonify(videos)

def validate_request(request_body):
    attributes = ["postal_code", "name", "phone"]
    for attribute in attributes:
        if attribute not in request_body:
            return {"details": f"Request body must include {attribute}."}, 400


