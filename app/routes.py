from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime
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
                    
                    
                    
                    



    
















    
# # RENTAL ENDPOINTS
# @rental_bp.route('/check-out', methods=['POST'])
# def handle_checkout():
#     response_body = request.get_json()
#     new_checkout = Rental(customer_id=response_body['customer_id'],
#                             video_id=response_body['video_id'],
#                             due_date=response_body['due_date'],
#                             videos_checked_out_count=response_body['videos_checked_out_count'],
#                             # Need to figure out how to calculate available_inventory -- see Wave 2 ReadMe
#                             available_inventory=response_body['available_inventory'])
#     db.session.add(new_checkout)
#     db.session.commit()

#     return make_response({"customer_id": new_checkout.customer_id,
#                             "video_id": new_checkout.video_id,
#                             "due_date": new_checkout.due_date,
#                             "videos_checked_out_count": new_checkout.videos_checked_out_count,
#                             "available_inventory": new_checkout.available_inventory})
    

# @rental_bp.route('/check-in', methods=['POST'])
# def handle_checkin():
#     pass