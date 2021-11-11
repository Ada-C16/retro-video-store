from app import db
from app.models.customer import Customer
from datetime import date 
from flask import Blueprint, jsonify, request


customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("", methods = ["GET"])
def get_customers():
    """
    Retrieves all saved customer records
    """
    customer = Customer.query.all()
    customer_response = [customer.to_json() for customer in customer]
    return jsonify(customer_response), 200


@customer_bp.route("", methods = ["POST"])
def post_customer():
    """
    Allows client to create new customer records,
    which must have name, phone number, and
    postal_code in request_body
    """
    request_body = request.get_json() 
    if "name" not in request_body:
        return jsonify(details="Request body must include name."), 400
    if "postal_code" not in request_body:
        return jsonify(details="Request body must include postal_code."), 400
    if "phone" not in request_body:
        return jsonify(details="Request body must include phone."), 400
    
    new_customer = Customer(
        name=request_body["name"],
        phone=request_body["phone"],
        postal_code=request_body["postal_code"],
    )
    db.session.add(new_customer)
    db.session.commit()

    return{
        "id": new_customer.id,
        "name": new_customer.name,
        "phone": new_customer.phone,
        "postal_code": new_customer.postal_code,
    }, 201


@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"]) 
def handle_customer_id(customer_id):
    """
    Allows client to retrieve, post, and delete customer records
    only after ensuring that the customer_id is an integer.
    """
    try: 
        customer_id = int(customer_id)
    except:
        return jsonify(None), 400
    
    customer = Customer.query.get(customer_id)
    
    if customer == None:
        return jsonify(message=f"Customer {customer_id} was not found"), 404

    elif request.method == "GET":
        return {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            }, 200

    elif request.method == "PUT":
        form_data = request.get_json()

        if "name" not in form_data or "phone" not in form_data \
        or "postal_code" not in form_data:
            return jsonify(None), 400

        customer.name = form_data["name"]
        customer.phone = form_data["phone"]
        customer.postal_code = form_data["postal_code"]

        db.session.commit()

        return {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }, 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return {
            "id": customer.id
        }, 200