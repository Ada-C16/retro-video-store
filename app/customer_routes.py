import re
from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request, abort

customer_bp = Blueprint("customers",__name__, url_prefix="/customers")

def valid_int(id,parameter_type):
    try:
        int(id)
    except :
        abort(make_response({"error":f"{parameter_type} must be an integer"},400))
    
def get_customer_from_id(id):
    valid_int(id, "id")
    customer = Customer.query.get(id)
    if customer:
        return customer
    abort(make_response({"message": f"Customer {id} was not found"}, 404))

#CUSTOMER ROUTES
#GET
@customer_bp.route("/<id>", methods=["GET"])
def get_customer(id):
    customer = get_customer_from_id(id)
    response_body = customer.to_dict()

    return jsonify(response_body)


@customer_bp.route("", methods = ["GET"])
def get_customers():
    customers= Customer.query.all()
    customer_response=[]

    for customer in customers:
        customer_response.append(customer.to_dict())

    return jsonify(customer_response)
    

#POST 
@customer_bp.route("", methods = ["POST"])
def create_customer():
    form_data = request.get_json()

    if "phone" not in form_data:
        return make_response({"details":"Request body must include phone."},400)

    if "postal_code" not in form_data: 
        return make_response({"details":"Request body must include postal_code."},400)

    if "name" not in form_data:
        return make_response({"details":"Request body must include name."},400)


    new_customer = Customer(
        name = form_data["name"],
        postal_code = form_data["postal_code"],
        phone = form_data["phone"],
    )

    db.session.add(new_customer)
    db.session.commit()
    response_body ={"id":new_customer.id}
    return make_response(jsonify(response_body), 201)
    

#PUT
@customer_bp.route("/<id>", methods = ["PUT"])
def update_customer(id):
    customer = get_customer_from_id(id)
    form_data = request.get_json()

    if  "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
            response_body = {"details": "Invalid data"}
            return make_response(jsonify(response_body), 400)

    customer.name = form_data["name"]
    customer.phone = form_data["phone"]
    customer.postal_code = form_data["postal_code"]
    
    db.session.commit()

    return make_response(jsonify(customer.to_dict()), 200)


#DELETE
@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):
    customer = get_customer_from_id(id)
    db.session.delete(customer)
    db.session.commit()
    response_body= {"id": customer.id}
    return make_response(jsonify(response_body), 200)


