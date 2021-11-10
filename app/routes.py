from app import db
from flask import Blueprint
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------

# GET CUSTOMERS ALL

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    
    for customer in customers:
        customers_response.append(customer.to_json())
    
    return jsonify(customers_response), 200


# GET CUSTOMER BY ID
@customers_bp.route("/<id>", methods=["GET"])
def get_customer(id):
    if not id.isdigit():
        return jsonify({"message": "Invalid ID"}), 400    
    
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
    else:
        jsonify(customer.to_json()), 200
        

# POST CUSTOMER
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    elif "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    elif "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400
    
    new_customer = Customer(
        name = request_body["name"], 
        postal_code = request_body["postal_code"], 
        phone = request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
        
    return jsonify({"id": new_customer.id}), 201



# PUT CUSTOMER
@customers_bp.route("/<id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
        
    request_body = request.get_json()
    customer.name=request_body["name"] 
    customer.postal_code=request_body["postal_code"] 
    customer.phone=request_body["phone"] 
    
    # if not customer.name.isalpha() or not customer.phone.name.isalpha() or not customer.postal_code.isalpha() or "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
    #     return 400
    
    # elif "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
    #     return 400
    
    db.session.commit()
    return jsonify(customer.to_json()), 200
    


# DELETE CUSTOMER
@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": (f"Customer {id} was not found")}), 404
    else:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.id}), 200
    
    
    

# --------------------------------
# ----------- RENTALS ----------
# --------------------------------

# POST /rentals/check-out

@rentals_bp.route("/check_out", methods=["POST"])
def checkout_video():
    pass



# POST /rentals/check-in

@rentals_bp.route("/check_in", methods=["POST"])
def checkin_video():
    pass
    
    
# GET /customers/<id>/rentals  
# FOR A SPECIFIC CUSTOMER, GET ALL VIDEO RENTALS
@customers_bp.route("/<id>/rentals", methods=["GET"])
def rentals_by_specific_customer():
    
    #get the customer
    customer = Customer.query.get(id)
    if customer is None:
        # return jsonify({"message": (f"Customer {id} was not found")}), 404
        return 404
    
    #get all the rentals and filter for that customer
    rentals = ...
    
    #make formated list of rentals for response
    
  



# GET /videos/<id>/rentals  
# FOR A SPECIFIC VIDEO, GET ALL CUSTOMERS CURRENTLY RENTING
@videos_bp.route("/<id>/rentals", methods=["GET"])
def rentals_of_specific_video():
   
    #get the specific video
    video = Video.query.get(id)
    if video is None:
        # return jsonify({"message": (f"Customer {id} was not found")}), 404
        return 404
    
    #get all the rentals for that specific video
    rentals = ...
    
    # find and make a list of all the customers for all the returned rentals of the specific video
    customers = []