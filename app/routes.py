from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone, date, timedelta

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix=("/videos"))
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix=("/rentals"))



@rentals_bp.route("/check-out", methods=["POST"])
def handle_rentals_out():
    # if request.method == "POST":
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")
    due_date = date.today() + timedelta(days=7)

    customer = Customer.query.get(customer_id)
    if customer_id is None:
        return jsonify(None), 400
    if customer is None:
        return jsonify(None), 404

    video = Video.query.get(video_id)
    if video_id is None:
        return jsonify(None), 400
    if video is None:
        return jsonify(None), 404
    

    video_checked_out_count = Rental.query.filter_by(video_id=video_id, checked_in_status=False).count()
    available_inventory = video.total_inventory - video_checked_out_count

    if available_inventory == 0:
        return jsonify({
            "message" : "Could not perform checkout"
        }), 400

    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        due_date=due_date
    )

    db.session.add(new_rental)
    db.session.commit()

    video_checked_out_count = Rental.query.filter_by(video_id=video_id).count()
    available_inventory = video.total_inventory - video_checked_out_count

    return {
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": video_checked_out_count,
        "available_inventory": available_inventory 
        }, 200
 
@rentals_bp.route("/check-in", methods=["POST"])
def handle_rentals_in():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    customer = Customer.query.get(customer_id)
    if customer_id is None:
        return jsonify(None), 400
    if customer is None:
        return jsonify(None), 404

    video = Video.query.get(video_id)
    if video_id is None:
        return jsonify(None), 400
    if video is None:
        return jsonify(None), 404

    rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id, checked_in_status=False).order_by(Rental.due_date.asc()).first()
    if rental is None:
        return jsonify({"message" : f"No outstanding rentals for customer {customer_id} and video {video_id}"
        }), 400

    rental.checked_in_status = True
    video_checked_out_count = Rental.query.filter_by(video_id=video_id, checked_in_status=False).count()
    available_inventory = video.total_inventory - video_checked_out_count

    db.session.commit()

    return {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "videos_checked_out_count": video_checked_out_count,
        "available_inventory": available_inventory 
        }, 200

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def list_customer_rentals(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({
            "message" : f"Customer {customer_id} was not found"
        }), 404
    customer_rentals = Rental.query.filter_by(customer_id=customer_id, checked_in_status=False).all()
    customer_rentals_response = []
    for customer_rental in customer_rentals:
        video = Video.query.get(customer_rental.video_id)
        customer_rentals_response.append({
            "release_date" : video.release_date,
            "title" : video.title,
            "due_date" : customer_rental.due_date
        })
    return jsonify(customer_rentals_response)


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def list_video_rentals(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({
            "message" : f"Video {video_id} was not found"
        }), 404
    video_rentals = Rental.query.filter_by(video_id=video_id, checked_in_status=False).all()
    video_rentals_response = []
    for video_rental in video_rentals:
        customer = Customer.query.get(video_rental.customer_id)
        video_rentals_response.append({
            "due_date" : video_rental.due_date,
            "name" : customer.name,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code
        })
    return jsonify(video_rentals_response)


@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                "id": video.id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            })
        
        return jsonify(videos_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        title = request_body.get("title")
        release_date = request_body.get("release_date")
        total_inventory = request_body.get("total_inventory")

        if not title:
            return jsonify({
                "details" : "Request body must include title."
            }), 400
        
        if not release_date:
            return jsonify({
                "details" : "Request body must include release_date."
            }), 400
        
        if not total_inventory:
            return jsonify({
                "details" : "Request body must include total_inventory."
            }), 400
        
        new_video = Video(
            title=title,
            release_date=release_date,
            total_inventory=total_inventory
        )
        db.session.add(new_video)
        db.session.commit()

        return {
            "id": new_video.id,
            "title" : new_video.title,
            "total_inventory" : new_video.total_inventory
        }, 201


@videos_bp.route("/<video_id>", methods= ["GET", "PUT", "DELETE"])
def handle_video(video_id):
    if not video_id.isnumeric():
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify({
            "message" : f"Video {video_id} was not found"
        }), 404

    if request.method == "GET":
        return jsonify({
            "id" : video.id,
            "title" : video.title,
            "release_date" : video.release_date,
            "total_inventory" : video.total_inventory
        }), 200
    
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id" : video.id
        }), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        title = request_body.get("title")
        release_date = request_body.get("release_date")
        total_inventory = request_body.get("total_inventory")

        if not (title and release_date and total_inventory):
            return jsonify({
                "details" : "Invalid data"
            }), 400
        
        video.title = title
        video.release_date = release_date
        video.total_inventory = total_inventory

        db.session.commit()

        return jsonify({
            "id" : video.id,
            "title" : video.title,
            "release_date" : video.release_date,
            "total_inventory" : video.total_inventory,
        }), 200

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

