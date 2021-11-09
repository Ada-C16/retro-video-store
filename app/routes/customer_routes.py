from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
# videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["GET"])
def get_customers():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        customers = Customer.query.order_by(Customer.name).all()
    elif sort_query == "desc":
        customers = Customer.query.order_by(Customer.name.desc()).all()
    else:
        customers = Customer.query.all()

    response_body = [customer.to_dict() for customer in customers]
    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    if customer_id.isdigit() == False:
        return jsonify(None), 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify({'message': f'Customer {customer_id} was not found'}), 404

    response_body = customer.to_dict()

    return jsonify(response_body), 200

@customers_bp.route("", methods=["POST"])
def post_new_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    elif "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    elif "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400

    new_customer = Customer(name=request_body["name"],
    postal_code=request_body["postal_code"],
    phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    response_body = {
        "id": new_customer.customer_id
    }
    return jsonify(response_body), 201

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer is None:
        return jsonify({'message': f'Customer {customer_id} was not found'}), 404

    request_body = request.get_json()
    
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    elif "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    elif "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400

    
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    response_body = customer.to_dict()

    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({'message': f'Customer {customer_id} was not found'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({
        'id': customer.customer_id
        }), 200

