from flask import Blueprint, jsonify, request, make_response, abort
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# Blueprints
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#Helper Functions
def is_id_valid(id):
    try:
        int(id)
    except:
        abort(make_response(jsonify({"message": "Please input valid id number"}), 400))
    return id

def validate_data(request_body, required_attributes):
    for attribute in required_attributes:
        if attribute not in request_body:
            abort(make_response(jsonify({"details": f"Request body must include {attribute}."}), 400))
    return request_body

#Videos routes
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    video_list = []
    videos = Video.query.all()

    for video in videos:
        video_list.append(video.to_dict())
    
    return make_response(jsonify(video_list), 200)

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_video(video_id):
    video_id = is_id_valid(video_id)
    video = Video.query.get(video_id)

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 

    if request.method == "GET":
        return make_response(jsonify(video.to_dict()), 200)
    
    elif request.method == "DELETE":
        if not video.rentals:
            db.session.delete(video)
            db.session.commit()
            return make_response(jsonify({"id": int(video_id)}), 200)
        else:
            active_rentals = Rental.query.filter_by(video_id=f"{video.id}")
            for rental in active_rentals:
                db.session.delete(rental)
            db.session.delete(video)
            db.session.commit()
            return make_response("", 200)
    
    elif request.method == "PUT":
        required_attributes = ["title", "release_date", "total_inventory"]
        request_body = validate_data(request.get_json(), required_attributes)

        video.title = request_body["title"]
        video.total_inventory = request_body["total_inventory"]
        video.release_date = request_body["release_date"]

        db.session.commit()

        return make_response(jsonify(video.to_dict()), 200)

# @videos_bp.route("/<video_id>", methods=["DELETE"])
# def delete_one_video(video_id):
#     video = Video.query.get(video_id)
#     if not video:
#         return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 
#     else:
#         if not video.rentals:
#             db.session.delete(video)
#             db.session.commit()
#             return make_response(jsonify({"id": int(video_id)}), 200)
#         else:
#             active_rentals = Rental.query.filter_by(video_id=f"{video.id}")
#             for rental in active_rentals:
#                 db.session.delete(rental)
#             db.session.delete(video)
#             db.session.commit()
#             return make_response("", 200)


@videos_bp.route("", methods=["POST"])
def create_new_video():
    required_attributes = ["title", "release_date", "total_inventory"]
    request_body = validate_data(request.get_json(), required_attributes)

    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"]    
)
    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)

# @videos_bp.route("/<video_id>", methods=["PUT"])
# def update_video(video_id):
#     video = Video.query.get(video_id)
#     required_attributes = ["title", "release_date", "total_inventory"]
#     request_body = validate_data(request.get_json(), required_attributes)

#     if not video:
#         return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404) 

#     video.title = request_body["title"]
#     video.total_inventory = request_body["total_inventory"]
#     video.release_date = request_body["release_date"]

#     db.session.commit()

#     return make_response(jsonify(video.to_dict()), 200)


# Customer routes
@customers_bp.route("", methods=["POST"])
def create_customer():
    required_attributes = ["postal_code", "name", "phone"]
    request_body = validate_data(request.get_json(), required_attributes)

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = date.today()
        )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers_list = []
    customers = Customer.query.all()

    for customer in customers:
        customers_list.append(customer.to_dict())

    return make_response(jsonify(customers_list), 200)

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    required_attributes = ["postal_code", "name", "phone"]
    customer_id = is_id_valid(customer_id)
    customer = Customer.query.get(customer_id)
    customer_id = int(customer_id)

    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)

    elif request.method == "GET":
        return make_response(jsonify(customer.to_dict()), 200)

    elif request.method == "DELETE":
        if not customer.rentals:
            db.session.delete(customer)
            db.session.commit()
            return make_response(jsonify({"id": int(customer_id)}), 200)
        else:
            active_rentals = Rental.query.filter_by(customer_id=f"{customer.id}")
            for rental in active_rentals:
                db.session.delete(rental)
            db.session.delete(customer)
            db.session.commit()
            return make_response("", 200)

    elif request.method == "PUT":
        request_body = validate_data(request.get_json(), required_attributes)

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return make_response(jsonify(customer.to_dict()), 200)


#Rental Endpoints
@rentals_bp.route("/<rental_status>", methods=["POST"])
def rental_status(rental_status):
    required_attributes = ["customer_id", "video_id"]
    request_body = validate_data(request.get_json(), required_attributes)

    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    if not customer or not video:
        return make_response("", 404)

    rental = Rental(customer_id = int(customer.id),
                video_id = int(video.id),
                due_date = datetime.utcnow() + timedelta(days=7))

    dict_rent = rental.to_dict()

    if rental_status == "check-out":
        if video.total_inventory == 0:
            return make_response(jsonify({"message": "Could not perform checkout"}), 400)
        else:
            video.total_inventory -= 1
            customer.number_of_rentals += 1
            rental.status = "checked-out"

        db.session.add(rental)
        db.session.commit()
    
    elif rental_status == "check-in":

        if video.title not in customer.customer_rentals_titles():
            return make_response(jsonify({"message": "No outstanding rentals for customer 1 and video 1"}), 400)

        else:
            rental.status = "checked-in"
            customer.number_of_rentals -= 1 
            video.total_inventory += 1
            db.session.commit()

    dict_rent["videos_checked_out_count"] = customer.number_of_rentals
    dict_rent["available_inventory"] = video.total_inventory
        
    return make_response(jsonify(dict_rent), 200)

@videos_bp.route('/<video_id>/rentals', methods=["GET"])
def get_rentals_for_customer(video_id):
    video_id = is_id_valid(video_id)
    video = Video.query.get(video_id)

    if not video:
        return make_response(jsonify({"message": f"Video {video_id} was not found"}), 404)

    rentals = video.video_rentals() 
    return make_response(jsonify(rentals), 200)

@customers_bp.route('/<customer_id>/rentals', methods=["GET"])
def get_rentals_for_customer(customer_id):
    customer_id = is_id_valid(customer_id)
    customer = Customer.query.get(customer_id)

    if not customer:
        return make_response(jsonify({"message": f"Customer {customer_id} was not found"}), 404)

    rentals = customer.customer_rentals() 
    return make_response(jsonify(rentals), 200)