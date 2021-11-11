from flask import Blueprint, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
import datetime

# setup blueprints here
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# Customers routes

# WV1 returns empty list if no customers, otherwise, list of dictionaries
# summarizing each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()
    response = [customer.to_dict() for customer in customers]
    return jsonify(response)

# WV1 adds new customer to customers. 400 error if phone, name, or 
# postal code are missing from request body. 
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def post_customers():
    response_body = request.get_json()
    if not Customer.is_data_valid(response_body)[0]:
        return Customer.is_data_valid(response_body)[1], 400
    else:
        new_customer = Customer.from_json(response_body)
    
    db.session.add(new_customer)
    db.session.commit()
    return {"id": new_customer.customer_id}, 201

# WV1 Get data about one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer.
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        return customer.to_dict(), 200


# WV1 Update one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer, or
# if input data is invalid.
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:
        response_body = request.get_json()
    if not Customer.is_data_valid(response_body)[0]:
        return Customer.is_data_valid(response_body)[1], 400
    customer.name = response_body["name"]
    customer.postal_code = response_body["postal_code"]
    customer.phone = response_body["phone"]
    db.session.commit()
    return customer.to_dict(), 200


# WV1 Delete one specific customer by ID. 404 error if customer of
# specified ID is not found. 400 error if ID is not an integer.
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    else:

        rental_ids = Rental.query.with_entities(Rental.rental_id).filter(Rental.customer_id == int(customer_id))
        for rental_id in rental_ids:
            db.session.delete(Rental.query.get(rental_id)) # look into backref cascade? to make the tables do this automatically
        db.session.commit()

        db.session.delete(customer)
        db.session.commit()
        return {"id": customer.customer_id}, 200


# Video routes

#WV1: Get No Saved Videos Get Videos One Saved Video
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    videos = Video.query.all()
    response = [video.to_dict() for video in videos]
    return jsonify(response), 200

#WV1: Create Video, Must Contain Title/Release Date/Inventory
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_all_videos():
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

#WV1: Invalid Video ID, Get Video Not Found, Get Video
@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    try:
        video_id = int(video_id)
        video = Video.query.get(video_id)
    except ValueError:
        return {}, 400
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    else:
        return jsonify(video.to_dict()), 200

#WV1: Update Video, Update Video Not Found, Invalid Data
@videos_bp.route("/<video_id>", methods=["PUT"])
def update_one_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    input_data = request.get_json()
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    try:
        video.title = input_data["title"]
        video.release_date = input_data["release_date"]
        video.total_inventory = input_data["total_inventory"]
    except KeyError:
        if "title" not in input_data:
            return {}, 400
        if "release_date" not in input_data:
            return {}, 400
        if "total_inventory" not in input_data:
            return {}, 400
    db.session.commit()
    return jsonify(video.to_dict()), 200

#WV1: Delete Video, Delete Video Not Found
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    else:
        db.session.delete(video)
        db.session.commit()
        return {"id": video_id}, 200

# Rentals

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    request_body = request.get_json()

    if not Rental.is_data_valid(request_body):
        return {}, 400
    # might need to validate data
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    due_date = datetime.date.today() + datetime.timedelta(days=7)
    new_rental = Rental(video_id=video_id, customer_id=customer_id, due_date=due_date)
    video = Video.query.get_or_404(video_id)
    customer = Customer.query.get_or_404(customer_id)

    total_inventory = video.total_inventory
    checked_out = Rental.query.filter(Rental.video_id == video_id).count()
    
    if checked_out == total_inventory:
        return {"message": "Could not perform checkout"}, 400
    
    db.session.add(new_rental)
    db.session.commit()

    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "due_date": due_date,
        "videos_checked_out_count": checked_out + 1,
        "available_inventory": total_inventory - checked_out - 1
    }, 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json()

    if not Rental.is_data_valid(request_body):
        return {}, 400
    # might need to validate data
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    video = Video.query.get_or_404(video_id)
    customer = Customer.query.get_or_404(customer_id)

    rental = Rental.query.filter(Rental.video_id == video_id, Rental.customer_id == customer_id)
    if rental.count() == 0:
        return {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400
    rental_id = rental[0].rental_id
    rental = Rental.query.get(rental_id)
    # Rental.query.get({"video_id": video_id, "customer_id": customer_id,})
    db.session.delete(rental)
    db.session.commit()

    total_inventory = video.total_inventory
    checked_out = Rental.query.filter(Rental.video_id == video_id).count()

    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": checked_out,
        "available_inventory": total_inventory - checked_out
    }, 200

# Rentals x Customers

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_customer(customer_id):
    if not Customer.is_int(customer_id):
        return {'message': f'{customer_id} is not a valid customer id'}, 400
    customer = Customer.query.get(customer_id)
    if not customer:
        return {'message': f'Customer {customer_id} was not found'}, 404
    video_ids = Rental.query.with_entities(Rental.video_id).filter(Rental.customer_id == int(customer_id))
    result = [Video.query.get(id).to_dict() for id in video_ids]
    return jsonify(result), 200