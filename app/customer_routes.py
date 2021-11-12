from app.models.customer import Customer
from flask import Blueprint, make_response, request, jsonify, abort
from app import db
from app.validate import Validate

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

# having to do validation in nearly every funcion, is there a way to only do it once and pass around?


@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    try:
        new_customer = Customer(
            name=request_body["name"],
            phone=request_body["phone"],
            postal_code=request_body["postal_code"],
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify(new_customer.to_dict()), 201

    except KeyError:
        return make_response(Validate.missing_fields(request_body, Customer), 400)


@customer_bp.route("", methods=["GET"])
def get_all():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])


@customer_bp.route("/<id>", methods=["GET"])
def get_one(id):
    customer_id = Validate.valid_id(id)
    customer = Validate.valid_customer(customer_id)
    return customer.to_dict()


@customer_bp.route("/<id>", methods=["PUT"])
def update_cutomer(id):
    customer_id = Validate.valid_id(id)
    customer = Validate.valid_customer(customer_id)
    request_body = request.get_json()
    missing = Validate.missing_fields(request_body, Customer)

    if not missing:
        customer.update(request_body)
        db.session.commit()
        return customer.to_dict()
    else:
        abort(400)


@customer_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer_id = Validate.valid_id(id)
    customer = Validate.valid_customer(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.id}


@customer_bp.route("/<id>/rentals", methods=["GET"])
def get_customer_rentals(id):

    customer_id = Validate.valid_id(id)
    customer = Validate.valid_customer(customer_id)

    rentals = customer.get_rentals()
    return jsonify(rentals), 200
