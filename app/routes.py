from flask import Blueprint, jsonify, make_response
from flask.globals import request
from app.models.customer import Customer 
from app.models.video import Video
from app.models.rental import Rental, due_date
from app import db
from datetime import date, datetime

from tests.test_wave_02 import CUSTOMER_ID


# --------------------------------
# -------- CUSTOMER ROUTES -------
# --------------------------------
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    missing = ""
    if "name" not in request_body:
        missing = "name"
    elif "postal_code" not in request_body:
        missing = "postal_code"
    elif "phone" not in request_body:
        missing = "phone"
    if missing:
        return {"details": f"Request body must include {missing}."}, 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return {"id": new_customer.id}, 201

@customers_bp.route("", methods=["GET"])
def read_customers():
    customers = Customer.query.all()

    response_body = []

    for customer in customers:
        response_body.append(customer.to_dict())
    
    return jsonify(response_body), 200

@customers_bp.route("/<id>", methods=["GET"])
def read_one_customer(id):
    try:
        int(id)
    except:
        return {"message": "Invalid data"}, 400

    customer = Customer.query.get(id)

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404        

    return customer.to_dict(), 200

@customers_bp.route("/<id>", methods=["PUT", "PATCH"])
def update_customer(id):
    request_body = request.get_json()

    customer = Customer.query.get(id)

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404

    if "name" not in request_body or "phone" not in request_body \
    or "postal_code" not in request_body:
        return {"details": "Invalid request"}, 400

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    db.session.commit()

    return customer.to_dict(), 200

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.id}, 200


# --------------------------------
# -------- VIDEO ROUTES ----------
# --------------------------------
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def read_videos():
    videos = Video.query.all()

    response_body = []

    if not videos:
        return jsonify([]), 200

    for video in videos:
        response_body.append(video.to_dict())
    
    return jsonify(response_body), 200

@videos_bp.route("/<id>", methods=["GET"])
def read_one_video(id):
    try:
        int(id)
    except: 
        return {"message": "Invalid data"}, 400

    video = Video.query.get(id)

    if not video:
        return {"message": f"Video {id} was not found"}, 404        

    return video.to_dict(), 200 

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    missing = ""
    if "title" not in request_body:
        missing = "title"
    elif "release_date" not in request_body:
        missing = "release_date"
    elif "total_inventory" not in request_body:
        missing = "total_inventory"
    if missing:
        return {"details": f"Request body must include {missing}."}, 400

    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )
    
    db.session.add(new_video)
    db.session.commit()

    return new_video.to_dict(), 201


@videos_bp.route("/<id>", methods=["PUT", "PATCH"])
def update_videos(id):
    videos = Video.query.get(id)
    request_body= request.get_json()

    if not videos:
        return {"message": f"Video {id} was not found"}, 404

    if "title" not in request_body or "release_date" not in request_body \
    or "total_inventory" not in request_body:
        return {"details": "Invalid request"}, 400

    videos.title = request_body["title"]
    videos.release_date = request_body["release_date"]
    videos.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return videos.to_dict(), 200

@videos_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video = Video.query.get(id)

    if not video:
        return {"message": f"Video {id} was not found"}, 404

    db.session.delete(video)
    db.session.commit()

    return {"id": video.id}, 200

# --------------------------------
# -------- RENTAL ROUTES ---------
# --------------------------------
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    missing = ""
    if "customer_id" not in request_body:
        missing = "customer_id"
    elif "video_id" not in request_body:
        missing = "video_id"
    if missing:
        return {"details": f"Request body must include {missing}."}, 400
    
    video = Video.query.get(request_body["video_id"])
    if not video:
        return {"message": "Video not found"}, 404

    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return {"message": "Customer not found"}, 404

    if not video.get_available_inventory():
        return {"message": "Could not perform checkout"}, 400
     
    new_rental = Rental(
        customer_id=request_body["customer_id"],
        video_id=request_body["video_id"],
        due_date=due_date()
    )

    db.session.add(new_rental)
    db.session.commit()

    return new_rental.to_dict(), 200

#either delete the rental or change it's status to "checked_in"
@rentals_bp.route("/check-in", methods=["POST"])
def check_in_rental():
    request_body = request.get_json()

    missing = ""
    if "customer_id" not in request_body:
        missing = "customer_id"
    elif "video_id" not in request_body:
        missing = "video_id"
    if missing:
        return {"details": f"Request body must include {missing}."}, 400
    
    video = Video.query.get(request_body["video_id"])
    if not video:
        return {"message": "Video not found"}, 404

    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return {"message": "Customer not found"}, 404
    
    #the video and customer do not match a current rental
    matching_rental = Rental.query.filter(Rental.customer_id == customer.id, Rental.video_id == video.id ).first()
    if not matching_rental:
        return {"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}, 400

    db.session.delete(matching_rental)
    db.session.commit()

    return matching_rental.to_dict(), 200

@customers_bp.route("/<customer_id>/rentals")
def read_rentals_by_customer(customer_id):
    customer = Customer.query.get(customer_id)
    customer_rentals = Rental.query.filter(Rental.customer_id == customer_id).all()

    rentals_response = []

    if not customer:
        return {"message": f"Customer {customer_id} was not found"}, 404
    
    for item in customer_rentals:
        id = item.video_id
        rentals_response.append(item.get_rental_by_customer(id))

    return jsonify(rentals_response), 200

@videos_bp.route("/<video_id>/rentals")
def read_rentals_by_video(video_id):
    video = Video.query.get(video_id)
    video_rentals = Rental.query.filter(Rental.video_id == video_id).all()

    rentals_response = []    

    if not video:
        return {"message": f"Video {video_id} was not found"}, 404

    for item in video_rentals:
        id = item.customer_id
        rentals_response.append(item.get_rental_by_video(id))
    
    return jsonify(rentals_response), 200