from app.models.customer import Customer
from flask import Blueprint, make_response, request, jsonify, abort
from app import db

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


def missing_fields(request_body):
    required_fields = ["name", "phone", "postal_code"]

    for field in required_fields:
        if field not in request_body:
            return {"details": f"Request body must include {field}."}
    return False


def valid_customer(id):
    try:
        id = int(id)
    except ValueError:
        abort(400)
    customer = Customer.query.get(id)
    if customer:
        return customer

    abort(make_response({"message": f"Customer {id} was not found"}, 404))


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
        return make_response(missing_fields(request_body), 400)


@customer_bp.route("", methods=["GET"])
def get_all():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])


@customer_bp.route("/<id>", methods=["GET"])
def get_one(id):
    customer = valid_customer(id)
    return customer.to_dict()


@customer_bp.route("/<id>", methods=["PUT"])
def update_cutomer(id):
    customer = valid_customer(id)
    request_body = request.get_json()
    missing = missing_fields(request_body)

    if not missing:
        customer.update(request_body)
        db.session.commit()
        return customer.to_dict()
    else:
        abort(400)


@customer_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = valid_customer(id)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.id}
