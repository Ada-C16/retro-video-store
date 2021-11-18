from flask import abort,Blueprint,jsonify,request,make_response
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
import requests, os
from dotenv import load_dotenv
from datetime import datetime, timedelta




customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
load_dotenv()


@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():

    if request.method == "GET":
        customers = Customer.query.all()
        
        customers_response = []

        for customer in customers:
            customers_response.append(customer.to_dict())      
        return jsonify(customers_response), 200
        

    elif request.method == "POST":

        request_body = request.get_json()

        if "name" not in request_body: 
            return make_response({"details": "Request body must include name."}, 400) 
        
        elif "postal_code" not in request_body: 
            return make_response({"details": "Request body must include postal_code."}, 400) 

        elif "phone" not in request_body: 
            return make_response({"details": "Request body must include phone."}, 400) 
        else:
            new_customer = Customer(name=request_body["name"], phone=request_body["phone"], postal_code=request_body["postal_code"]) 

        db.session.add(new_customer)
        db.session.commit()
        return make_response({"id": new_customer.id}, 201)



@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    if customer_id.isnumeric() != True:
        return {"details" : "Invalid request"}, 400
    customer = Customer.query.get(customer_id)
    
    
    if request.method == "GET":
        if customer is None:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        
        return make_response(customer.to_dict(), 200)

    elif request.method == "DELETE":
        if customer is None:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)

        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": int(customer_id)}, 200)

    if request.method == "PUT":
        request_body = request.get_json()
        if customer is None:
            return make_response({"message": f"Customer {customer_id} was not found"}, 404)
        elif  "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        else:
            response_body = request.get_json()
        
        customer.name = response_body["name"]
        customer.phone = response_body["phone"]
        customer.postal_code = response_body["postal_code"]
    
        db.session.commit()
        return make_response(customer.to_dict(), 200)



@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():

# Wave 1 GET/videos and no saved videos
    if request.method == "GET":
        videos = Video.query.all()
        
        videos_response = []

        for video in videos:
            videos_response.append(video.to_dict())      
        return jsonify(videos_response), 200

# Wave 1 POST/videos and video must contain title, video must contain release_date, and video must contain total_inventory
    elif request.method == "POST":

        request_body = request.get_json()

        if "title" not in request_body: 
            return make_response({"details": "Request body must include title."}, 400) 
        
        elif "release_date" not in request_body: 
            return make_response({"details": "Request body must include release_date."}, 400) 

        elif "total_inventory" not in request_body: 
            return make_response({"details": "Request body must include total_inventory."}, 400) 
        else:
            new_video = Video(title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"]) 

        db.session.add(new_video)
        db.session.commit()
        return make_response({"id": new_video.id, "title": new_video.title, "total_inventory": new_video.total_inventory}, 201)

# Wave 1 GET/DELETE/PUT
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    response_body = [video.to_dict() for video in videos]
    return jsonify(response_body), 200

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_video(video_id):
    if video_id.isnumeric() != True:
        return {"details" : "Invalid request"}, 400
    video = Video.query.get(video_id)
    
    
    if request.method == "GET":
        if video is None:
            return make_response({"message": f"Video {video_id} was not found"}, 404)

        
        return make_response(video.to_dict(), 200)

    elif request.method == "DELETE":
        if video is None:
            return make_response({"message": f"Video {video_id} was not found"}, 404)

        db.session.delete(video)
        db.session.commit()
        
        return make_response({"id": int(video_id)}, 200)

    if request.method == "PUT":
        request_body = request.get_json()
        if video is None:
            return make_response({"message": f"Video {video_id} was not found"}, 404)
        elif  "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        else:
            response_body = request.get_json()
        
        video.title = response_body["title"]
        video.release_date = response_body["release_date"]
        video.total_inventory = response_body["total_inventory"]
    
        db.session.commit()
        return make_response(video.to_dict(), 200)







# WAVE 2

@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    try:
        customer_id = int(request_body["customer_id"])
        video_id = int(request_body["video_id"])
    except ValueError:
        return jsonify({"Error": "Customer ID and Video ID must be integers."}), 400


    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    elif video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    if video.total_inventory == 0:
        return jsonify({"message": f"Video {video_id} is out of stock"}), 404

    if "customer_id" not in request_body: 
        return jsonify({"details": "Request body must include customer_id."}), 400
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400

    new_rental = Rental(customer_id=request_body["customer_id"],
        video_id=request_body["video_id"])
        # videos_checked_out_count=request_body["videos_checked_out_count"],
        # available_inventory=request_body["available_inventory"]) 


    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.to_dict()), 200


@rentals_bp.route("/check_in", methods=["POST"])
def handle_rentals():
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 404
    elif "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 404

    new_rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"],
    due_date=datetime.now())

    db.session.add(new_rental)
    db.session.commit()


    new_video = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": None,
            "available_inventory": None
        }
    return new_video, 201

@customers_bp.route("/<customer_id>/rentals")
def read_customer_rentals(id):
    customer = Customer.query.get(id)
    customer_rentals = Rental.query.filter(Rental.customer_id == id).all()

    response = []

    if not customer:
        return {"message": f"Customer {id} was not found"}, 404

    for item in customer_rentals:
        response.append(item.rental_dict(item.video_id))

    return jsonify(response), 200

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

