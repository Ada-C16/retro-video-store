from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request, make_response
import requests
from datetime import datetime, timedelta

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# create
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
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
def get_customers():
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
    if customer_id.isnumeric() != True:
        return jsonify({"error": "Invalid Data"}), 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404
        # refactor with helper function
    response_body = {
        "id": customer.customer_id,
        "name": customer.name,
        "registered_at": customer.registered_at,
        "postal_code": customer.postal_code,
        "phone": customer.phone}
    return jsonify(response_body), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    if "name" not in request_body or type(customer.name) != str:
        return make_response("", 400)
    if "postal_code" not in request_body or type(customer.postal_code) != str:
        return make_response("", 400)
    if "phone" not in request_body or type(customer.phone) != str:
        return make_response("", 400)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.add(customer)
    db.session.commit()

    response_body= {
                "id": customer.customer_id,
                "name": customer.name,
                "registered_at": customer.registered_at,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
            }


    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_one_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()
    
    return {"id": customer.customer_id}















@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Request body must include title."}), 400
    if "release_date" not in request_body:
        return jsonify({"details": "Request body must include release_date."}), 400
    if "total_inventory" not in request_body:
        return jsonify({"details": "Request body must include total_inventory."}), 400

    # elif "register_at" not in request_body:
    #     return jsonify({"details": "Invalid data"}), 400

    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"],
    )
    db.session.add(new_video)
    db.session.commit()

    response_body = {


        "id": new_video.video_id,
        "title": new_video.title,
        "release_date": new_video.release_date,
        "total_inventory": new_video.total_inventory,

    }

    return jsonify(response_body), 201


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    video_response = []

    for video in videos:
        video_response.append({
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        })
    return jsonify(video_response)

    # sort_query = request.args.get("sort")
    # # account for the asc/desc in wave 2(?)
    # if sort_query == "asc":
    #     tasks = Task.query.order_by(Task.title.asc())
    # elif sort_query == "desc":
    #     tasks = Task.query.order_by(Task.title.desc())
    # else:
    #     tasks = Task.query.all()

    # dd each task to be returned


@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):

    # customer = Customer.query.get_or_404(customer_id)
    if video_id.isnumeric() != True:
        return jsonify({"error": "Invalid Data"}), 400

    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404
        # refactor with helper function
    response_body = {
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }
    return jsonify(response_body), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def update_one_video(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    if "title" not in request_body:
        return make_response("", 400)
    if "release_date" not in request_body :
        return make_response("", 400)
    if "total_inventory" not in request_body:
        return make_response("", 400)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.add(video)
    db.session.commit()

    response_body= {
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }


    return jsonify(response_body), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_one_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    db.session.delete(video)
    db.session.commit()
    
    return {"id": video.video_id}


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_vid():
    request_body = request.get_json()
    

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response("", 400)
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video is None or customer is None:
        return jsonify(""), 404

    

    num_current_checked_out =  Rental.query.filter_by(video_id=video.video_id, videos_checked_in=False).count() 
    current_available_inventory = video.total_inventory - num_current_checked_out

    if current_available_inventory == 0:
        return jsonify({ 
                "message": "Could not perform checkout"
                }), 400
    
    new_rental = Rental(customer_id=customer.customer_id,\
    video_id=video.video_id, 
    due_date=(datetime.now() + timedelta(days=7)))

    db.session.add(new_rental)
    db.session.commit()

    num_videos_checked_out =  Rental.query.filter_by(video_id=video.video_id, videos_checked_in=False).count() #.count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(customer_id=customer.customer_id, videos_checked_in=False).count() 

    response_body = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": videos_checked_out_count ,
            "available_inventory": available_inventory 
        }
    return jsonify(response_body), 200











@rentals_bp.route("/check-in", methods=["POST"])
def check_in_vid():
    request_body = request.get_json()
    

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response("", 400)
    
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video is None or customer is None:
        return jsonify(""), 404

    

    # num_current_checked_out =  Rental.query.filter_by(video_id=video.video_id, videos_checked_in=False).count() 
    # current_available_inventory = video.total_inventory - num_current_checked_out

    # if current_available_inventory == 0:
    #     return jsonify({ 
    #             "message": "Could not perform checkout"
    #             }), 400
    
    # new_rental = Rental(customer_id=customer.customer_id,\
    # video_id=video.video_id, 
    # due_date=(datetime.now() + timedelta(days=7)))
    
    rental = Rental.query.filter_by(video_id=video.video_id,customer_id=customer.customer_id, videos_checked_in=False).first()
    
    if rental is None:
        return jsonify({"message": f"No outstanding rentals for customer {customer.customer_id} and video {video.video_id}"}), 400
    
    rental.videos_checked_in = True


    num_videos_checked_out =  Rental.query.filter_by(video_id=video.video_id, videos_checked_in=False).count() #.count() returns length
    available_inventory = video.total_inventory - num_videos_checked_out

    videos_checked_out_count = Rental.query.filter_by(customer_id=customer.customer_id, videos_checked_in=False).count() 
    
    
    db.session.commit()
    response_body = {
            "customer_id": rental.customer_id,
            "video_id": rental.video_id,
        
            "videos_checked_out_count": videos_checked_out_count ,
            "available_inventory": available_inventory 
        }
    return jsonify(response_body), 200
