from app import db
from app.models.customer import Customer 
from flask import Blueprint, jsonify, request
import datetime
from datetime import timedelta
from sqlalchemy import select
from app.models.video import Video
from app.models.rental import Rental

NOW = datetime.datetime.now()
DUE_DATE = NOW + timedelta(days=7)

# Blueprints
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Customer helper functions
def display_customer_info(customer):
    return {
        "id": customer.id,
        "name": customer.name,
        "postal_code": customer.postal_code,
        "phone": customer.phone
    }

def customer_not_found(customer_id):
    return {"message" : f"Customer {customer_id} was not found"}

# customers endpoint

# returns list of all existing customers
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    if customers is None:
        return jsonify("Not Found"), 404

    customer_response = []
    for customer in customers:
        customer_response.append({
            "id": customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone})


    return jsonify(customer_response), 200


# returns one instance of a specific customer 
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400
    
    customer = Customer.query.get(customer_id)

    if customer == None:
        response_body = {"message" : f"Customer {customer_id} was not found"}
        return jsonify(response_body), 404
    
    response_body = {"id": customer.id, "name": customer.name, "postal_code": customer.postal_code, "phone": customer.phone}

    return jsonify(response_body), 200


# creates a new customer
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    if "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    if "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
        )

    db.session.add(new_customer)
    db.session.commit()

    return ({
        "id": new_customer.id,
        "name": new_customer.name,
        "postal_code": new_customer.postal_code,
        "phone": new_customer.phone
    }), 201


# updates an exsiting customers record
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_existing_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id), 404


    request_body = request.get_json()
    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        return jsonify("Bad Request"), 400

    customer.name = request_body.get("name")
    customer.postal_code = request_body.get("postal_code")
    customer.phone = request_body.get("phone")
    customer.registered_at = datetime.now()

    db.session.commit()
    response_body = ({
            "name": f"{customer.name}",
            "postal_code": f"{customer.postal_code}",
            "phone": f"{customer.phone}"})

    return response_body, 200


# delete an exsiting customer record
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_existing_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id), 404

    db.session.delete(customer)
    db.session.commit()

    return {
        "id": customer.id
        }, 200


# *****************************
# *** videos endpoint  CRUD ***
# *****************************

# READ
# get all existing video records
@videos_bp.route("", methods = ["GET"])
def get_videos():
    videos = Video.query.all()
    
    if videos == None:
        return [], 200

    response_body = [video.to_dict() for video in videos]

    return jsonify(response_body), 200

# get one video record via id number
@videos_bp.route("/<video_id>", methods = ["GET"])
def get_video(video_id):

    # check that </video_id> is valid input (ie an id number)
    if not video_id.isnumeric():
        return jsonify(None), 400
    
    video = Video.query.get(video_id)
    
    if video == None:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    response_body = video.to_dict()

    return jsonify(response_body), 200

# CREATE
# post a video record
@videos_bp.route("", methods = ["POST"])
def post_video():
    request_body = request.get_json()

    if "title" not in request_body:
        response_body = {"details": "Request body must include title."}
        return jsonify(response_body), 400
    elif "release_date" not in request_body:
        response_body = {"details": "Request body must include release_date."}
        return jsonify(response_body), 400
    elif "total_inventory" not in request_body:
        response_body = {"details": "Request body must include total_inventory."}
        return jsonify(response_body), 400

    new_video = Video.from_dict(request_body)

    db.session.add(new_video)
    db.session.commit()

    response_body = new_video.to_dict()

    return jsonify(response_body), 201

# UPDATE
# update a video record
@videos_bp.route("<video_id>", methods = ["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    
    if video is None:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    form_data = request.get_json()
    
    if "title" not in form_data or "total_inventory" not in form_data or "release_date" not in form_data:
        return jsonify(None), 400

    video.title = form_data["title"]
    video.total_inventory = form_data["total_inventory"]
    video.release_date = form_data["release_date"]

    db.session.commit()

    response_body = video.to_dict()

    return jsonify(response_body), 200


# DELETE
# delete a video record
@videos_bp.route("/<video_id>", methods = ["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        response_body = {"message": f"Video {video_id} was not found"}
        return jsonify(response_body), 404
    else:
        response_body = {"id" : video.id}

        db.session.delete(video)
        db.session.commit()

        return jsonify(response_body), 200

# *****************************
# *** POST custom endpoints ***
# *****************************

# POST /rentals/check-out
# changed bp to rentals vs videos
@rentals_bp.route("/check-out", methods = ["POST"])
def post_rentals_check_out():
    request_body = request.get_json()

    # check for valid input
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    # this is the customer id of the customer who has this rental
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    # check if customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify("ther is no customer with that id num"), 404

    # check if video exists
    video = Video.query.get(video_id)
    if not video:
        # response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify("Not Found"), 404
    
    # check if video is in stock
    if video.total_inventory - len(video.rentals) < 1:
        return {"message": "Could not perform checkout"}, 400 

    # create a new rental instance
    new_rental = Rental(
        due_date=DUE_DATE,
        customer_id=customer.id,
        video_id=video.id
    )

    # add new_rental instance to the database
    db.session.add(new_rental)
    db.session.commit()

    # create a response body
    response_body = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": len(customer.videos),
            "available_inventory": video.total_inventory - len(video.rentals)
        }

    return jsonify(response_body), 200
    # return jsonify(new_rental.due_date), 200


# POST /rentals/check-in
# changed bp to rentals vs videos
@rentals_bp.route("/check-in", methods = ["POST"])
def post_rentals_check_in():
    request_body = request.get_json()
    
    # check for valid input
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400

    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    # this is the customer id of the customer who has this rental
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    # check if customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        response_body = {"message" : f"Customer {customer_id} was not found"}
        return jsonify(response_body),404

    # check if video exists
    video = Video.query.get(video_id)
    if not video:
        response_body = {"message" : f"Video {video_id} was not found"}
        return jsonify(response_body), 404

    # logic for counting number of check-ins
    checked_in_count = len(video.rentals) - 1

    rentals = customer.rentals
    if not rentals:
        return {"message": "No outstanding rentals for customer 1 and video 1"}, 400 

    for rental in rentals:
        response_body = {
            "customer_id": rental.customer_id,
            "video_id" : rental.video_id,
            "videos_checked_out_count" : (len(customer.videos) - 1),
            "available_inventory" : (video.total_inventory - checked_in_count) 
        }   

    # delete the rental record
    db.session.delete(rental)
    db.session.commit()

    return jsonify(response_body), 200



# *****************************
# *** GET custom endpoints ***
# *****************************
@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_checked_out_videos(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message" : f"Customer {customer_id} was not found"}, 404
    
    checked_out = []
    rentals = customer.rentals
    videos = customer.videos
    for rental in rentals:
        for video in videos:
            checked_out.append({
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date
                })

    return jsonify(checked_out), 200

@rentals_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_with_rental(customer_id):
    customer = Customer.query.get(customer_id)
    rentals = customer.rentals
    for rental in rentals:
        db.session.delete(rental)
        db.session.delete(customer)

        db.session.commit()

    return {
        "message": f"Customer {customer.name} has been deleted from the system...FOREVER"
        }, 200