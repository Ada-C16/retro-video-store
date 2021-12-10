from app import db
from flask import Blueprint
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime, timedelta


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------


# GET ALL CUSTOMERS
@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_json())
    return jsonify(customers_response), 200


# CREATE CUSTOMER
@customers_bp.route("", methods=["POST"])
def create_customer():
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
    return jsonify(new_customer.to_json()), 201


# GET CUSTOMER BY ID
@customers_bp.route("/<id>", methods=["GET"])
def get_customer(id):
    if id.isnumeric() != True:
        return {"message": "Customer id provided is not a number."}, 400
    customer = Customer.query.get(id)
    if customer is None:
        return {"message": f"Customer {id} was not found"}, 404
    else:
        return jsonify(customer.to_json()), 200


# UPDATE CUSTOMER BY ID
@customers_bp.route("/<id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        return {"message": f"Customer {id} was not found"}, 404
    if request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        elif "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    db.session.commit()
    return jsonify(customer.to_json()), 200


# DELETE CUSTOMER BY ID
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
# ----------- VIDEOS ----------
# --------------------------------


# GET ALL VIDEOS
@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_json())
    return jsonify(videos_response), 200


# CREATE VIDEO
@videos_bp.route("", methods=["POST"])
def create_video():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return {"details": "Request body must include title."}, 400
        elif "release_date" not in request_body:
            return {"details": "Request body must include release_date."}, 400
        elif "total_inventory" not in request_body:
            return {"details": "Request body must include total_inventory."}, 400
        new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        return jsonify(new_video.to_json()), 201


# GET VIDEO BY ID
@videos_bp.route("/<id>", methods=["GET"])
def get_video(id):
    if id.isnumeric() != True:
        return {"message": "Video id provided is not a number."}, 400
    video = Video.query.get(id)
    if video is None:
        return {"message": f"Video {id} was not found"}, 404
    if request.method == "GET":
        return jsonify(video.to_json()), 200


# UPDATE VIDEO BY ID
@videos_bp.route("/<id>", methods=["PUT"])
def update_video(id):
    video = Video.query.get(id)
    if video is None:
        return {"message": f"Video {id} was not found"}, 404
    if request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body:
            return {"details": "Request body must include title."}, 400
        elif "release_date" not in request_body:
            return {"details": "Request body must include release_date."}, 400
        elif "total_inventory" not in request_body:
            return {"details": "Request body must include total_inventory."}, 400
        video.title = request_body["title"]
        video.request_body = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.to_json()), 200


# DELETE VIDEO BY ID
@videos_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video = Video.query.get(id)
    if video is None:
        return {"message": f"Video {id} was not found"}, 404
    db.session.delete(video)
    db.session.commit()
    return {"id": video.id}, 200


# --------------------------------
# ----------- RENTALS ----------
# --------------------------------


# CHECK OUT A VIDEO TO A CUSTOMER
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    # check if customer and video exist
    if customer is None or video is None:
        return make_response("", 404)
    num_of_videos_rented = Rental.query.filter_by(
        video_id=video.id, checked_out=True).count()
    available_inventory = video.total_inventory - num_of_videos_rented
    if available_inventory == 0:
        return jsonify({"message": f"Could not perform checkout"}), 400
    new_rental = Rental(customer_id=customer.id,
                        video_id=video.id,
                        due_date=(datetime.now() + timedelta(days=7)),
                        checked_out=True)
    db.session.add(new_rental)
    db.session.commit()
    videos_checkout_by_customer = Rental.query.filter_by(
        customer_id=customer.id, checked_out=True).count()
    available_inventory -= 1
    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": videos_checkout_by_customer, "available_inventory": available_inventory}), 200


# CHECK IN A VIDEO TO A CUSTOMER
@rentals_bp.route("/check-in", methods=["POST"])
def checkin_video():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    elif "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    # check if customer and video exist
    if customer is None or video is None:
        return make_response("", 404)
    rental = Rental.query.filter_by(
        video_id=video.id, customer_id=customer.id, checked_out=True).first()
    if rental is None:
        return jsonify({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}), 400
    rental.checked_out = False
    db.session.commit()
    num_of_videos_rented = Rental.query.filter_by(
        video_id=video.id, checked_out=True).count()
    available_inventory = video.total_inventory - num_of_videos_rented
    videos_checkout_by_customer = Rental.query.filter_by(
        customer_id=customer.id, checked_out=True).count()
    return jsonify({
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "videos_checked_out_count": videos_checkout_by_customer, "available_inventory": available_inventory}), 200


# GET RENTALS BY CUSTOMER
@customers_bp.route("/<id>/rentals", methods=["GET"])
def rentals_by_video(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({"message": f"Customer {id} was not found"}), 404
    rentals = Rental.query.filter_by(
        customer_id=customer.id, checked_out=True).all()
    rentals_response = []
    for rental in rentals:
        video_id = rental.video_id
        video = Video.query.get(video_id)
        rentals_response.append(video.rental_dict(rental))
    return jsonify(rentals_response), 200


# GET RENTALS BY VIDEO
@videos_bp.route("/<id>/rentals", methods=["GET"])
def rentals_by_video(id):
    video = Video.query.get(id)
    if video is None:
        return jsonify({"message": f"Video {id} was not found"}), 404
    rentals = Rental.query.filter_by(video_id=video.id, checked_out=True).all()
    rentals_response = []
    for rental in rentals:
        customer_id = rental.customer_id
        customer = Customer.query.get(customer_id)
        rentals_response.append(customer.rental_dict(rental))
    return jsonify(rentals_response), 200
