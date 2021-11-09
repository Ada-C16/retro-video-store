from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from dotenv import load_dotenv
import os
from sqlalchemy import desc 


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")


def validate_id_int(id):
    try:
        id = int(id)
        return id
    except:
        abort(400, "Error: ID needs to be a number.")

def validate_request_body(request_body):
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400
    return False

# ---------------------------
# ------- CUSTOMERS ---------
# ---------------------------

# Posts new customer
@customers_bp.route("", methods = ["POST"])
def create_customer():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_request_body(request_body)
    if invalid:
        # Returns the invalid error message and status code
        return invalid
        
    # if "name" not in request_body:
    #     return jsonify({"details": "Request body must include name."}), 400
    # if "postal_code" not in request_body:
    #     return jsonify({"details": "Request body must include postal_code."}), 400
    # if "phone" not in request_body:
    #     return jsonify({"details": "Request body must include phone."}), 400

    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()

    new_customer_response = new_customer.to_dict()
    return jsonify(new_customer_response), 201

# Handles all customers
@customers_bp.route("", methods=["GET"])
def handle_customers():
    customers_response = []
    sort_by = request.args.get('sort')
    if sort_by == "asc":
        customers = Customer.query.order_by(Customer.name).all()
    elif sort_by == "desc":
        customers = Customer.query.order_by(desc(Customer.title)).all()
    else:
        customers = Customer.query.all()
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# Handles one customer
@customers_bp.route("/<id>", methods=["GET", "PUT"])
def handle_customer(id):
    id = validate_id_int(id)
    customer = Customer.query.get(id)
    if not customer:
        return make_response({"message": f"Customer {id} was not found"}, 404)
    if request.method == "GET":
        return jsonify(customer.to_dict()), 200
    elif request.method == "PUT":
        request_body = request.get_json()
        # Check if request_body is invalid/missing data
        invalid = validate_request_body(request_body)
        if invalid:
            # Returns the invalid error message and status code
            return invalid

        # if "name" not in request_body:
        #     return jsonify({"details": "Request body must include name."}), 400
        # if "postal_code" not in request_body:
        #     return jsonify({"details": "Request body must include postal_code."}), 400
        # if "phone" not in request_body:
        #     return jsonify({"details": "Request body must include phone."}), 400

        # customer.name=f"Updated ${request_body['name']}"
        # customer.postal_code=f"Updated ${request_body['postal_code']}"
        # customer.phone=f"Updated ${request_body['phone']}"
        customer.name=request_body["name"]
        customer.postal_code=request_body["postal_code"]
        customer.phone=request_body["phone"]

        db.session.commit()
        return jsonify(customer.to_dict()), 200

# ----- BELOW: PATCH ROUTE UNNEEDED SO FAR ------
# @customers_bp.route("<customer_id>/<patch_complete>", methods=["PATCH"])
# def patch_task(task_id, patch_complete):
#     task_id = validate_id_int(task_id)
#     task = Task.query.get(task_id)
#     if not task:
#         return make_response("", 404)
#     if patch_complete == "mark_complete":
#         task.completed_at=datetime.now()
#         # ID of the channel you want to send the message to
#         channel_id = "C02LA52J4AW"
#         SLACK_KEY = os.environ.get("SLACK_API_KEY")
#         text=f"Someone just completed the task {task.title}"
#         data = {
#             'channel': channel_id, 
#             'as_user': True,
#             'text': text
#         }
#         requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {SLACK_KEY}"}, data=data)
#     elif patch_complete == "mark_incomplete":
#         task.completed_at=None
#     db.session.commit()
#     return jsonify({"task": task.to_dict()}), 200

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    #print(id)
    id=validate_id_int(id)
    
    customer = Customer.query.get(id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": id}, 200)
    else:
        return make_response({"message": f"Customer {id} was not found"}, 404)