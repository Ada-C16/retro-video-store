from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix=("/videos"))


@videos_bp.route("", methods=["GET", "POST"])

def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "description": task.description,
                "is_complete": False if task.completed_at == None else True
            })




@videos_bp.route("/<video_id>", methods= ["GET", "PUT", "DELETE"])



@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        customers_response = []
        for customer in customers:
            customers_response.append({
                "id" : customer.id,
                "name" : customer.name,
                "registered_at" : customer.registered_at,
                "postal_code" : customer.postal_code,
                "phone" : customer.phone
            })

        return jsonify(customers_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        name = request_body.get("name")
        postal_code = request_body.get("postal_code")
        phone = request_body.get("phone")
        
        if not postal_code:
            return jsonify({
                "details" : "Request body must include postal_code."
            }), 400
        
        if not name:
            return jsonify({
                "details" : "Request body must include name."
            }), 400

        if not phone:
            return jsonify({
                "details" : "Request body must include phone."
            }), 400

        new_customer = Customer(
            name=name, 
            postal_code=postal_code, 
            phone=phone,
            registered_at=datetime.now(timezone.utc).strftime("%a, %d %b %Y %X %z")
            )

        db.session.add(new_customer)
        db.session.commit()

        return jsonify({
            "id" : new_customer.id
        }), 201

@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def handle_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400
        
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify({
            "message" : f"Customer {customer_id} was not found"
        }), 404

    if request.method == "GET":
        return jsonify({
            "id" : customer.id,
            "name" : customer.name,
            "registered_at" : customer.registered_at,
            "postal_code" : customer.postal_code,
            "phone" : customer.phone
        }), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        name = request_body.get("name")
        postal_code = request_body.get("postal_code")
        phone = request_body.get("phone")

        if not (name and postal_code and phone):
            return jsonify({
                "details" : "Invalid data"
            }), 400
        
        customer.name = name
        customer.postal_code = postal_code
        customer.phone = phone

        db.session.commit()

        return jsonify({
            "id" : customer.id,
            "name" : customer.name,
            "registered_at" : customer.registered_at,
            "postal_code" : customer.postal_code,
            "phone" : customer.phone
        }), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            "id" : customer.id
        }), 200
>>>>>>> bacd02f44bd396d3d659159dda3bf39149a0cb23
