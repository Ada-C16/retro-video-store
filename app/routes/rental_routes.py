from app import db
from app.models.customer import Customer
from .customer_routes import customer_bp
from .video_routes import video_bp
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response,request, abort
from dotenv import load_dotenv
import os
from datetime import date, timedelta, datetime



load_dotenv()
rental_bp = Blueprint("rental", __name__,url_prefix="/rentals")

#Helper function
def valid_int(number):
    try:
        return int(number)     
    except:
        abort(make_response({"error": f"{number} must be an int"}, 400))

   
#Helper function
def get_object_from_id(obj, id):
    id = valid_int(id) 
    obj1 = obj.query.get(id)
    if obj1:
        return obj1
    else:       
        abort(make_response(jsonify({"message": f"{obj.__str__(obj)} {id} was not found"}), 404))

@rental_bp.route("/check-out", methods=["POST"])
def create_customer_video():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
    
        return make_response({"message" : "bad request"}, 400)
    
    else:
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
        customer_checking_out = get_object_from_id(Customer, customer_id)
        video_to_be_checked_out = get_object_from_id(Video, video_id)
    
        if "videos_checked_out_count" not in request_body:
            videos_checked_out_count = 1
        due_date = datetime.today() + timedelta(days=7)

        total_inventory = video_to_be_checked_out.total_inventory
        available_inventory = total_inventory - videos_checked_out_count
        if total_inventory >= videos_checked_out_count:
            new_rental = Rental(video_id=video_id, customer_id=customer_id, videos_checked_out_count=videos_checked_out_count, due_date=due_date)
            video_to_be_checked_out.total_inventory = available_inventory
        else:
            return jsonify({"message":"Could not perform checkout"}), 400
        
        db.session.add(new_rental)
        db.session.commit()

        return make_response({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": due_date,
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory":available_inventory
        })

@rental_bp.route("/check-in", methods=["POST"])
def checkin_video():
    
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"message" : "bad request"}, 400)
    
  
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    checking_customer = get_object_from_id(Customer, customer_id)
    incoming_video = get_object_from_id(Video, video_id)
    
    rental_record = db.session.query(Rental).filter(Rental.customer_id==customer_id,Rental.video_id== Rental.video_id).first()

    if not rental_record:
            return make_response({"message": "No outstanding rentals for customer 1 and video 1"}, 400)
    else:
        if "videos_checked_out_count" not in request_body:
            videos_checked_out_count = 1  #this is incoming count from customer
        checked_out_now = rental_record.videos_checked_out_count - videos_checked_out_count  # previously\
        # recorded count minus the count customer returned
        
        this_video = Video.query.get(video_id)
        total_inventory = this_video.total_inventory
        available_inventory = total_inventory + videos_checked_out_count
        
        this_video.total_inventory = available_inventory
        
        
        response_dict = {
        "customer_id": rental_record.customer_id,
        "video_id": rental_record.video_id,
        "videos_checked_out_count": checked_out_now,
        "available_inventory":available_inventory
        }

        db.session.delete(rental_record)
        db.session.commit()

        return make_response(response_dict)


@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def rentals_by_customers(customer_id):

    one_customer = get_object_from_id(Customer, customer_id) 
    cust_videos = [video.to_dict() for video in one_customer.videos]
    return make_response(jsonify(cust_videos))


@video_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_video(video_id):
    one_video = get_object_from_id(Video, video_id)
    video_customers = [customer.to_dict() for customer in one_video.customers]
    return make_response(jsonify(video_customers))
