from flask import Blueprint, jsonify, make_response, request
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
        pass

# RENTAL ENDPOINTS
@rental_bp.route('/check-out', methods=['POST'])
def handle_checkout():
    # For calculating due date
    today = datetime.now()
    seven_days = timedelta(days=+7)

    request_body = request.get_json()

    if 'customer_id' not in request_body.keys() :
            return make_response({"details": "Request body must include customer."}, 404)
    elif 'video_id' not in request_body.keys():
            return make_response({"details":"Request body must include video."}, 404)
    # Does checking for available inventory belong here or inside the else block?
    elif request_body['available_inventory'] == 0:
            return make_response({"details": "All videos currently checked out."}, 400)
    else:
        # Do I need these? I'm using these to access the specific video and customer objects that match video_id and customer_id
        # I'm using these bc the rental instance hasn't been created yet.
        customer = Customer.query.get(request_body['customer_id'])
        video = Video.query.get(request_body['video_id'])

        new_checkout = Rental(customer_id=request_body['customer_id'],
                                video_id=request_body['video_id'],
                                due_date=today+seven_days

                                # Need to figure out how to calculate videos_checked_out_count
                                    # Can I use a class method?
                                # videos_checked_out_count= Use get_videos_checked_out_count()
                                    # I need to add 1 to videos_checked_out_count

                                # Need to figure out how to calculate available_inventory -- see Wave 2 ReadMe
                                    # Can I use a class method?
                                # available_inventory= Use calculate_available_inventory()
                                    # I need to subtract all copies currently checked out by all customers from total_inventory
                                        # all copies currently checked out = all videos_checked_out_count added up from all customers
                                            # Do I need to Rental.query.all() --> filter all videos_checked_out_count values and add them?
                                            # OR can also do Rental.query.all() --> filter by video_id and add instances of rentals that have the same video_id
                                )
        db.session.add(new_checkout)
        db.session.commit()

        return make_response({"customer_id": new_checkout.customer_id,
                                "video_id": new_checkout.video_id,
                                "due_date": new_checkout.due_date,
                                "videos_checked_out_count": new_checkout.videos_checked_out_count,
                                "available_inventory": new_checkout.available_inventory})


@rental_bp.route('/check-in', methods=['POST'])
def handle_checkin():
    request_body = request.get_json()
    rental_to_delete = Rental.query.get(request_body['video_id'])

    if 'customer_id' not in request_body.keys() :
            return make_response({"details": "Request body must include customer."}, 404)
    elif 'video_id' not in request_body.keys():
            return make_response({"details":"Request body must include video."}, 404)
    # Does checking for available inventory belong here or inside the else block?
    elif request_body['video_id'] not in request_body.values() and request_body['customer_id'] not in request_body.values():
            return make_response({"details": "The video and customer information do not match the current rental"}, 400)

    rental_deleted_confirmation =  Rental(customer_id=request_body['customer_id'],
                                video_id=request_body['video_id'],
                                due_date=request_body['due_date'] # What value do I put here? Do I use None?

                                # Need to figure out how to calculate videos_checked_out_count
                                    # Can I use a class method?
                                # videos_checked_out_count= Use get_videos_checked_out_count()
                                    # I need to subtract 1 from videos_checked_out_count

                                # Need to figure out how to calculate available_inventory -- see Wave 2 ReadMe
                                    # Can I use a class method?
                                # available_inventory= Use calculate_available_inventory()
                                    # I need to add one to available_inventory 
                                )

    # Delete the rental - am I deleting a rental instance currently that already exists due to the video being rented?
    db.session.delete(rental_to_delete)
    db.session.commit()

    # Make a response
    return make_response({"customer_id": rental_deleted_confirmation.customer_id,
                            "video_id": rental_deleted_confirmation.video_id,
                            "videos_checked_out_count": rental_deleted_confirmation.videos_checked_out_count,
                            "available_inventory": rental_deleted_confirmation.available_inventory})