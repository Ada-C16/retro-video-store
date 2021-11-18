from flask import abort,Blueprint,jsonify,request,make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime, timedelta
import requests



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


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

        if "name" not in request_body: #or not isinstance(request_body["name"], str):
            return make_response({"details": "Request body must include name."}, 400) 
        
        elif "postal_code" not in request_body: #or not isinstance(request_body["postal_code"], str):
            return make_response({"details": "Request body must include postal_code."}, 400) 

        elif "phone" not in request_body: #or not isinstance(request_body["phone"], str):
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





# @videos_bp.route("", methods=["GET"])
# def get_all_videos():
#     videos = Video.query.all()
#     response_body = [video.to_dict() for video in videos]
#     return jsonify(response_body), 200

# @videos_bp.route("", methods=["POST"])
# def post_videos():
#     request_body = request.get_json()
    
    
    # try:
    #     new_video = Video(title = request_body["title"],
    #         release_date = request_body["release_date"],
    #         total_inventory = request_body["total_inventory"])
    # except KeyError:
    #     if "title" not in request_body:
    #         return jsonify({"details": "Request body must include title."}), 400
    #     if "release_date" not in request_body:
    #         return jsonify({"details": "Request body must include release_date."}), 400    
    #     if "total_inventory" not in request_body:
    #         return jsonify({"details": "Request body must include total_inventory."}), 400
    # db.session.add(new_video)
    # db.session.commit()
    # return jsonify(new_video.to_dict()), 201

    






