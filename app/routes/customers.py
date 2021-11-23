from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.rental import Rental
from app.models.video import Video
from app.routes.helper_functions import * 


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_customers():
    customer_objects = Customer.query.all()
    response_list = []
    for customer in customer_objects:
        response_list.append(customer.to_dict())
    return make_response(jsonify(response_list), 200)

# Get one
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    selected_customer = get_customer_from_id(customer_id)
    return make_response(selected_customer.to_dict(), 200)

# Add customer
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def add_customer():
    request_body = request.get_json()
    if "postal_code" not in request_body:
        response_body = {"details": "Request body must include postal_code."}
        response = abort(make_response(response_body, 400))   
    if "name" not in request_body:
        response_body = {"details": "Request body must include name."}
        response = abort(make_response(response_body, 400)) 
    if "phone" not in request_body:
        response_body = {"details": "Request body must include phone."}
        response = abort(make_response(response_body, 400))
    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
    )
    db.session.add(new_customer)
    db.session.commit() 
    response = make_response(new_customer.to_dict(), 201)
    return response

# Delete customer
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    selected_customer = get_customer_from_id(customer_id)
    db.session.delete(selected_customer)
    db.session.commit()
    return make_response({"id": int(customer_id)}, 200)

# Update customer
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    selected_customer = get_customer_from_id(customer_id)
    request_body = request.get_json()
    if "name" in request_body:
        selected_customer.name = request_body["name"]
    else:
        abort(make_response({"error": "Invalid input"},400)) 
    if "phone" in request_body:
        selected_customer.phone = request_body["phone"]
    else:
        abort(make_response({"error": "Invalid input"},400)) 
    if "postal_code" in request_body:
        selected_customer.postal_code = request_body["postal_code"]
    else:
        abort(make_response({"error": "Invalid input"},400)) 
    db.session.commit()
    response_body = jsonify(selected_customer.to_dict())
    return make_response(response_body, 200)

# Get rentals by customer id
@customers_bp.route("/<id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_customer_id(id):
    get_customer_from_id(id)
    rentals = Rental.query.filter_by(customer_id=id).all()
    response_body = []
    for rental in rentals:
        video = get_video_by_id(rental.video_id)
        response_body.append({"release_date": video.release_date,
                            "title": video.title,
                            "due_date": rental.due_date})
    return make_response(jsonify(response_body), 200)