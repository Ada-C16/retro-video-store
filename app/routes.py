from flask import abort,Blueprint,jsonify,request,make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime
import requests


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    # customer_response = []

    if request.method == "GET":
        customers = Customer.query.all()
        response = [customer.to_dict() for customer in customers]
        return jsonify(response), 200

    elif request.method == "POST":
        customers = Customer.query.all()

        request_body = request.get_json()

        if "name" not in request_body or not isinstance(request_body["name"], str):
            return make_response({"details": "Request body must include name."}, 400) 
        
        elif "postal_code" not in request_body or not isinstance(request_body["postal_code"], str):
            return make_response({"details": "Request body must include postal_code."}, 400) 

        elif "phone" not in request_body or not isinstance(request_body["phone"], str):
            return make_response({"details": "Request body must include phone."}, 400) 
        else:
            new_customer = Customer(name=request_body["name"], phone=request_body["phone"], postal_code=request_body["postal_code"]) 

        db.session.add(new_customer)
        db.session.commit()
        return make_response({"id": new_customer.id}, 201)


def validate_endpoint_id(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        abort(make_response({f"details": "Endpoint must be an int."}, 400))

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    customer = Customer.query.get(customer_id)
    validate_endpoint_id(customer_id)

    if request.method == "GET":
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        # elif not isinstance(customer_id, int):
        #     return make_response({"message": f"{customer_id} is not a valid customer"}, 400)

        
        return make_response({customer.to_dict()}, 200)

    elif request.method == "DELETE":
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": int(customer_id)}, 200)

    if request.method == "PUT":
        request_body = request.get_json()
        if not customer:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)
        elif  "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        else:
            response_body = request.get_json()
        
        customer.name = response_body["name"]
        customer.phone = response_body["phone"]
        customer.postal_code = response_body["postal_code"]
    
        db.session.commit()
        return make_response({customer.to_dict()}, 200)


        # # return make_response({"customer": customer.to_dict()}, 200)
        # return make_response({"name": f"Updated {customer.name}" )

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return jsonify(response_body), 200

@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    
    try:
        new_video = Video(title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"])
    except KeyError:
        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        if "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400    
        if "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201

    






