from flask import Blueprint, jsonify, make_response, request
from flask.globals import _request_ctx_stack
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta
import requests

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')
video_bp = Blueprint('videos', __name__, url_prefix='/videos')
rental_bp = Blueprint('rentals', __name__, url_prefix='/rentals')

# VIDEO ENDPOINTS

@video_bp.route('', methods=['GET', 'POST'])
def handle_videos():
    if request.method == 'GET':
        videos = Video.query.all()
        videos_list = [{"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory
                        } for video in videos]
        return jsonify(videos_list)
    elif request.method == 'POST':
        request_body = request.get_json()
        if 'title' not in request_body.keys():
            return make_response({"details": "Request body must include title." }, 400)
        elif 'release_date' not in request_body.keys():
            return make_response({"details":"Request body must include release_date."}, 400)
        elif 'total_inventory' not in request_body.keys():
            return make_response({"details": "Request body must include total_inventory."}, 400)
        else:
            new_video = Video(title=request_body["title"], 
                                release_date=request_body["release_date"],
                                total_inventory=request_body["total_inventory"])

            db.session.add(new_video)
            db.session.commit()

            return make_response({"id": new_video.id,
                                    "title": new_video.title,
                                    "release_date": new_video.release_date,
                                    "total_inventory": new_video.total_inventory
                                                }, 201)

@video_bp.route('/<video_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_one_video(video_id):
    # Even though the end-user may type a number as an argument for video_id, its data type isn't automatically int.
    # The try/except clause coerces the typed argument to be an int. If it is a non-numeric value, then a ValueError will be raised.
    # Alternatively, can also use isnumeric(). This will return a boolean, so no need for try/except. An if/else clause will suffice.
    try:
        id = int(video_id)
    except ValueError:
        return jsonify({"details": "Invalid data"}), 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    one_video = {"title": video.title,
                "id": video.id,
                "total_inventory": video.total_inventory}

    if request.method == 'GET':
        return one_video
    elif request.method == 'PUT':
        updates = request.get_json()
        if 'title' not in updates.keys() or 'release_date' not in updates.keys() \
                                         or 'total_inventory' not in updates.keys():
            return make_response({"details": "Invalid data"}, 400)
        else:
            video.title = updates['title']
            video.release_date = updates['release_date']
            video.total_inventory = updates['total_inventory']

            db.session.commit()
            return make_response({"id": video.id,
                                    "title": video.title,
                                    "release_date": video.release_date,
                                    "total_inventory":video.total_inventory}) 
    elif request.method == 'DELETE':
        db.session.delete(video)
        db.session.commit()

        return make_response({"id": video.id})

@video_bp.route('/<id>/rentals', methods=['GET'])
def handle_rentals_by_video(id):
    video = Video.query.get(id)
    if video is None:
        return jsonify({"message": f"Video {id} was not found"}), 404
    else:
        rentals = Rental.query.filter_by(video_id=id, is_checked_in=False).all()
        customer_ids = [rental.customer_id for rental in rentals]

        customer_objs = []
        for customer_id in customer_ids:
            customer_obj = Customer.query.filter_by(id=customer_id).first()
            customer_dict = {"name": customer_obj.name}
            customer_objs.append(customer_dict)

        return jsonify(customer_objs)

# CUSTOMER ENDPOINTS

# Get all customers (no customer ids)
@customer_bp.route('', methods=['GET','POST'])
def handle_customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        customers_list = [{"id": customer.id,
                            "name": customer.name,
                            "postal_code": customer.postal_code,
                            "phone": customer.phone,
                            "registered_at": customer.registered_at} for customer in customers]
        return jsonify(customers_list)
    elif request.method == 'POST':
        request_body = request.get_json()
        if 'name' not in request_body.keys():
            return make_response({"details": "Request body must include name." }, 400)
        elif 'postal_code' not in request_body.keys():
            return make_response({"details":"Request body must include postal_code."}, 400)
        elif 'phone' not in request_body.keys():
            return make_response({"details": "Request body must include phone."}, 400)
        # elif 'registered_at' not in request_body.keys():
        #     return make_response({"details": "Request body must include registered_at."}, 400)
        else:
            new_customer = Customer(name=request_body["name"], 
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"])

            db.session.add(new_customer)
            db.session.commit()

            return make_response({"id": new_customer.id,
                                    "name": new_customer.name,
                                    "postal_code": new_customer.postal_code,
                                    "phone": new_customer.phone,
                                                }, 201)

@customer_bp.route('/<customer_id>', methods=['GET','PUT', 'DELETE'])
def handle_one_customer(customer_id):       
    try:
        id = int(customer_id)
    except ValueError:
        return jsonify({"details": "Invalid data"}), 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    
    one_customer = {"name": customer.name,
                    "id": customer.id,
                    "postal_code": customer.postal_code,
                    "phone": customer.phone}

    if request.method == 'GET': 
        return one_customer   
    elif request.method == 'PUT':
        updates = request.get_json()
        if 'name' not in updates.keys() or 'postal_code' not in updates.keys() \
                                         or 'phone' not in updates.keys():
            return make_response({"details": "Invalid data"}, 400)
        else:
            customer.name = updates['name']
            customer.postal_code = updates['postal_code']
            customer.phone = updates['phone']

            db.session.commit()
            return make_response({"id": customer.id,
                                    "name": customer.name,
                                    "postal_code": customer.postal_code,
                                    "phone":customer.phone}) 
    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()

        return make_response({"id": customer.id})
                    

# RENTAL ENDPOINTS
# Note: "dynamic" means an action (in this case, calculating available inventory) will be done a la minute 
# and does not need to be stored in the database. 

@rental_bp.route('/check-out', methods=['POST'])
def handle_checkout():
    request_body = request.get_json()

    if 'customer_id' not in request_body.keys():
        return make_response({"details": "Request must include customer id."}, 400)

    elif Customer.query.filter_by(id=request_body['customer_id']).first() is None:
        return make_response({"details": "Customer not found"}, 404)

    elif 'video_id' not in request_body.keys():
        return make_response({"details": "Request must include video id."}, 400)

    elif Video.query.filter_by(id=request_body['video_id']).first() is None:
            return make_response({"details": "Video not found"}, 404)
                
    # In SQL: SELECT * FROM videos WHERE video_id = self.id
        # Once specific video object is found, perform calculation
    available_inventory = Video.query.filter_by(id=request_body['video_id']).first().calculate_available_inventory()
    if available_inventory == 0:
        return make_response({"message": "Could not perform checkout"}, 400)

    else:
        new_rental = Rental(video_id=request_body["video_id"],
                            customer_id=request_body["customer_id"])
        
        db.session.add(new_rental)
        db.session.commit()
        
        videos_checked_out_count = Customer.query.filter_by(id=request_body['customer_id']).count()

        available_inventory_after_check_out = Video.query.filter_by(id=request_body['video_id']).first().calculate_available_inventory()

        return make_response({"id": new_rental.id,
                                "customer_id": new_rental.customer_id,
                                "video_id": new_rental.video_id,
                                "available_inventory": available_inventory_after_check_out,
                                "videos_checked_out_count": videos_checked_out_count})

@rental_bp.route('/check-in', methods=['POST'])
def handle_checkin():
    request_body = request.get_json()

    if "customer_id" not in request_body.keys():
        return make_response ({"details": "Customer ID required."}, 400)
    elif Customer.query.filter_by(id=request_body['customer_id']).first() is None:
        return make_response ({"details": "Customer not found."}, 404)
    elif 'video_id' not in request_body.keys():
        return make_response({"details": "Request must include video id."}, 400)
    elif Rental.query.filter_by(video_id=request_body['video_id']).first() is None and \
            Rental.query.filter_by(customer_id=request_body['customer_id']).first() is None:
        return make_response({
            "message": f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}, 400)
    
    elif not bool(Video.query.filter_by(id=request_body['video_id'])):
        return make_response({"details": "Video not found"}, 404)

    else:
        # Using the information from request_body, locate the rental whose status needs to be changed (i.e., the video is being returned)
        existing_rental = Rental.query.filter_by(video_id=request_body["video_id"], customer_id=request_body["customer_id"], \
                            is_checked_in=False).first()

        existing_rental.is_checked_in = True

        db.session.commit()

        available_inventory_after_checkin = Video.query.filter_by(id=request_body['video_id']).first().calculate_available_inventory()
        videos_checked_out_count = Customer.query.filter_by(id=request_body['customer_id']).first().get_videos_checked_out_count()

        return make_response({"video_id": existing_rental.video_id,
                                "customer_id": existing_rental.customer_id,
                                "videos_checked_out_count": videos_checked_out_count,
                                "available_inventory": available_inventory_after_checkin})






    
    
    # new_rental = Rental(video_id=request_body["video_id"],
    #                     customer_id=request_body["customer_id"])
    # updated_videos_checked_out = Customer.query.filter_by(id=request_body['customer_id']).first().videos_checked_out_count +1   
    # Customer.query.filter_by(id=request_body['customer_id']).first().videos_checked_out_count 



    # return make_response({"customer_id": request_body["customer_id"] ,
    #                           "video_id": request_body["video_id"]})

