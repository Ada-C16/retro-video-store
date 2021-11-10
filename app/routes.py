from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response
import requests
from datetime import datetime
import os
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")



# create
@customers_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "name" not in request_body: 
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:  
        return jsonify({"details": "Request body must include postal_code."}) , 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400 
    
    # elif "register_at" not in request_body:
    #     return jsonify({"details": "Invalid data"}), 400

    new_customer = Customer(
                    name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"],
                    )
    db.session.add(new_customer)
    db.session.commit()

    response_body = {
       
            
            "id": new_customer.customer_id,
            "name": new_customer.name,
            "postal_code": new_customer.postal_code,
            "phone": new_customer.phone,
            
        }
    
    return jsonify(response_body), 201


@customers_bp.route("", methods=["GET"])
def get_tasks():
        customers = Customer.query.all()
        customer_response = []
        
        for customer in customers:
            customer_response.append({
                "id": customer.customer_id,
                "name": customer.name,
                "registered_at": customer.registered_at,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
            })
        return jsonify(customer_response)
    


        # sort_query = request.args.get("sort")
        # # account for the asc/desc in wave 2(?)
        # if sort_query == "asc":
        #     tasks = Task.query.order_by(Task.title.asc())
        # elif sort_query == "desc":
        #     tasks = Task.query.order_by(Task.title.desc()) 
        # else:
        #     tasks = Task.query.all()

        # dd each task to be returned
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):

    # customer = Customer.query.get_or_404(customer_id)
    customer = Customer.query.get(customer_id)
    if customer_id.is_numeric():
        if customer is None:
            return {"message" : f"Customer {customer_id} was not found"}, 404


        # acconting for the descrepancy in wave 6 where it was saying to implement goal_id in thisresponse body.
        # fixed this by essentially "if there is a goal id at this task, then return that, if not, then return it without the goal id
        else:
            # if not task.goal_id:
            #     return {"task": {
            #         "id": task.task_id,
            #         "title": task.title,
            #         "description": task.description,
            #         "is_complete" : (False
            #         if task.completed_at == None else True)
            #         }},200


            # refactor with helper function
            response_body = {
                    "id": customer.customer_id,
                    "name": customer.name,
                    "registered_at": customer.registered_at,
                    "postal_code": customer.postal_code,
                    "phone": customer.phone,}
            return  jsonify(response_body), 200
    else:
        return make_response("", 400)

    