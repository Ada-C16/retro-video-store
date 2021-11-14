from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from dotenv import load_dotenv
import os
from sqlalchemy import desc
from datetime import date
from datetime import timedelta
# import datetime




customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")


def validate_id_int(id):
    try:
        id = int(id)
        return id
    except:
        abort(400, "Error: ID needs to be a number.")

def validate_customer_request_body(request_body):
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400
    return False

# ---------------------------
# ------- CUSTOMERS ---------
# ---------------------------

# Posts new customer
@customers_bp.route("", methods = ["POST"])
def create_customer():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_customer_request_body(request_body)
    if invalid:
        # Returns the invalid error message and status code
        return invalid
        
    # if "name" not in request_body:
    #     return jsonify({"details": "Request body must include name."}), 400
    # if "postal_code" not in request_body:
    #     return jsonify({"details": "Request body must include postal_code."}), 400
    # if "phone" not in request_body:
    #     return jsonify({"details": "Request body must include phone."}), 400

    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()

    new_customer_response = new_customer.to_dict()
    return jsonify(new_customer_response), 201

# Handles all customers
@customers_bp.route("", methods=["GET"])
def handle_customers():
    customers_response = []
    sort_by = request.args.get('sort')
    # Poss. Refactor: Could make a helper function, passing in sort_by as parameter
    if sort_by == "asc":
        customers = Customer.query.order_by(Customer.name).all()
    elif sort_by == "desc":
        customers = Customer.query.order_by(desc(Customer.title)).all()
    else:
        customers = Customer.query.all()
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# Handles one customer
@customers_bp.route("/<id>", methods=["GET", "PUT"])
def handle_customer(id):
    id = validate_id_int(id)
    customer = Customer.query.get(id)
    if not customer:
        return make_response({"message": f"Customer {id} was not found"}, 404)
    if request.method == "GET":
        return jsonify(customer.to_dict()), 200
    elif request.method == "PUT":
        request_body = request.get_json()
        # Check if request_body is invalid/missing data
        invalid = validate_customer_request_body(request_body)
        if invalid:
            # Returns the invalid error message and status code
            return invalid

        # if "name" not in request_body:
        #     return jsonify({"details": "Request body must include name."}), 400
        # if "postal_code" not in request_body:
        #     return jsonify({"details": "Request body must include postal_code."}), 400
        # if "phone" not in request_body:
        #     return jsonify({"details": "Request body must include phone."}), 400

        # customer.name=f"Updated ${request_body['name']}"
        # customer.postal_code=f"Updated ${request_body['postal_code']}"
        # customer.phone=f"Updated ${request_body['phone']}"
        customer.name=request_body["name"]
        customer.postal_code=request_body["postal_code"]
        customer.phone=request_body["phone"]

        db.session.commit()
        return jsonify(customer.to_dict()), 200

# ----- BELOW: PATCH ROUTE UNNEEDED SO FAR ------
# @customers_bp.route("<customer_id>/<patch_complete>", methods=["PATCH"])
# def patch_task(task_id, patch_complete):
#     task_id = validate_id_int(task_id)
#     task = Task.query.get(task_id)
#     if not task:
#         return make_response("", 404)
#     if patch_complete == "mark_complete":
#         task.completed_at=datetime.now()
#         # ID of the channel you want to send the message to
#         channel_id = "C02LA52J4AW"
#         SLACK_KEY = os.environ.get("SLACK_API_KEY")
#         text=f"Someone just completed the task {task.title}"
#         data = {
#             'channel': channel_id, 
#             'as_user': True,
#             'text': text
#         }
#         requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {SLACK_KEY}"}, data=data)
#     elif patch_complete == "mark_incomplete":
#         task.completed_at=None
#     db.session.commit()
#     return jsonify({"task": task.to_dict()}), 200

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    #print(id)
    id=validate_id_int(id)
    
    customer = Customer.query.get(id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": id}, 200)
    else:
        return make_response({"message": f"Customer {id} was not found"}, 404)

# ---------------------------
# --------- VIDEOS ----------
# ---------------------------

@videos_bp.route("", methods = ["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append(video.to_dict())

        return jsonify(videos_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response(
                {"details": "Request body must include title."}, 400
            )
        elif "release_date" not in request_body:
            return make_response(
                {"details": "Request body must include release_date."}, 400
            )
        elif "total_inventory" not in request_body:
            return make_response(
                {"details": "Request body must include total_inventory."}, 400
            )
        new_video = Video(
            title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        return make_response(
            new_video.to_dict(), 201
        )
            


@videos_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def handle_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return {"Error": "Id must be numeric"}, 400
    video = Video.query.get(video_id)
    if not video:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    if request.method == "GET":
        return video.to_dict()
        
    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(
                {"message": "Invalid data"}, 400
            )
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response(video.to_dict(), 200)


# ---------------------------
# -------- RENTALS ----------
# ---------------------------

# def create_due_date():
#     # date_1 = datetime.datetime.strptime(rental_date, "%y-%m-%d")
#     due_date = datetime.today() + datetime.timedelta(days=7)
#     return due_date

def validate_rental_request_body(request_body):
    if "customer_id" not in request_body:
        return jsonify({"details": "Request body must include customer_id."}), 400
    if "video_id" not in request_body:
        return jsonify({"details": "Request body must include video_id."}), 400
    return False

def get_available_inventory(request_body):
    videos = Video.query.get(request_body["video_id"])
    
    videos_in_rentals = Rental.query.filter_by(video_id=request_body["video_id"])


    available_inventory = videos.total_inventory - videos_in_rentals.count()
    return available_inventory
    # if available_inventory < 0:
    #     return "Could not perform checkout", 400
    # else:
    #     return available_inventory

# POST/Check-out a rental
@rentals_bp.route("/check-out", methods = ["POST"])
def create_rental():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_rental_request_body(request_body)

    if invalid:
        # Returns the invalid error message and status code
        return invalid
    
    due = date.today() + timedelta(days=7)
    new_rental_response = None
    
    validate_video_id = Video.query.get_or_404(request_body["video_id"])
    validate_customer_id = Customer.query.get_or_404(request_body["customer_id"])
    validate_inventory = get_available_inventory(request_body)
    if validate_inventory <= 0:
        return jsonify({"message": "Could not perform checkout"}), 400

    if validate_video_id and validate_customer_id and validate_inventory:
        new_rental = Rental(customer_id=request_body["customer_id"],
                        video_id=request_body["video_id"],
                        due_date=due

        )

        db.session.add(new_rental)
        db.session.commit()

        new_rental_response = new_rental.to_dict()

    # Calculate, then add to new_rental_response
    # for customer_id in Rental
    #     Video.query.get["customers"]:
    #     request_body["customer_id"]
    #     videos_count += 1
    #     #videos = Customer.query.get['videos']
    # videos_checked_out_count = Customer.query.get['videos']
    # Number of videos checked out by this customer_id
    # Count all rentals where customer_id is current rental's customer_id

        rentals = Rental.query.filter_by(customer_id=request_body["customer_id"])
    
        videos_checked_out_count = rentals.count()
        new_rental_response["videos_checked_out_count"] = videos_checked_out_count

    # video = Video.query.get(request_body["video_id"])
    
    # video_in_rentals = Rental.query.filter_by(video_id=request_body["video_id"])


    # available_inventory = video.total_inventory - video_in_rentals.count()
    # if available_inventory < 0:
    #     return "Could not perform checkout", 400
        after_check_out_inventory = get_available_inventory(request_body)
        
        new_rental_response["available_inventory"] = after_check_out_inventory

        videos_in_rental = Rental.query.filter_by(customer_id=request_body["customer_id"])    
        videos_checked_out_count = videos_in_rental.count()
        new_rental_response["videos_checked_out_count"] = videos_checked_out_count
        return new_rental_response
    # Count all rentals where video_id is current video_id
    # Then subract from total_inventory for video with this video_id

    return jsonify(new_rental_response), 200

# POST/Check-in a rental
@rentals_bp.route("/check-in", methods = ["POST"])
def update_rentals():
    request_body = request.get_json()
    if "video_id" not in request_body or "customer_id" not in request_body:
        return "Bad data", 400

    video = Video.query.get(request_body["video_id"])
    if not video:
        return make_response({"message":"Could not perform checkin"}, 404)

    customer = Customer.query.get(request_body["customer_id"])
    if not customer:
        return make_response({"message":"Could not perform checkin"}, 404)

    
    
    rentals = Rental.query.filter_by(customer_id=request_body["customer_id"], video_id=request_body["video_id"])
    # rental_response = []
    if not rentals.first():
        return make_response({"message": "No outstanding rentals for customer 1 and video 1"}, 400)
    # for rental in rentals:
    
    #     rental_response.append({"customer_id":rental.customer_id, "video_id": rental.video_id})
    db.session.delete(rentals.first())
    db.session.commit()
        
    videos_in_rental = Rental.query.filter_by(customer_id=request_body["customer_id"])    
    videos_checked_out_count = videos_in_rental.count()
    # rental_response[0]["videos_checked_out_count"] = videos_checked_out_count

    # video = Video.query.get(request_body["video_id"])
    video_in_rentals = Rental.query.filter_by(video_id=request_body["video_id"])


    available_inventory = video.total_inventory - video_in_rentals.count()
    if available_inventory < 0:
        return "Could not perform checkout", 400
    # rental_response[0]["available_inventory"] = available_inventory
    

    return {
        "customer_id": request_body["customer_id"],
        "video_id": request_body["video_id"],
        "videos_checked_out_count": videos_checked_out_count,
        "available_inventory": available_inventory

    }, 200



# @customers_bp.route("/<customer_id>/rentals", method=["GET"])
# def list_videos_by_customer(customer_id):
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         return make_response({"message": "Customer not found"}, 404)

#     videos = Rental.query.with_entities(Rental.video_id)




    





