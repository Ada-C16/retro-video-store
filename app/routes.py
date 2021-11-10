from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from dotenv import load_dotenv
import os
from sqlalchemy import desc
import datetime




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
    # Poss. Refactor: Could make 70 - 75 into a helper function, passing in sort_by as parameter
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

def create_due_date(rental_date):
    date_1 = datetime.datetime.strptime(rental_date, "%y-%m-%d")
    due_date = date_1 + datetime.timedelta(days=7)
    return due_date

def validate_rental_request_body(request_body):
    if "name" not in request_body:
        return jsonify({"details": "Request body must include name."}), 400
    if "postal_code" not in request_body:
        return jsonify({"details": "Request body must include postal_code."}), 400
    if "phone" not in request_body:
        return jsonify({"details": "Request body must include phone."}), 400
    return False

# Posts a rental
@rentals_bp.route("", methods = ["POST"])
def create_rental():
    request_body = request.get_json()
    # Check if request_body is invalid/missing data
    invalid = validate_rental_request_body(request_body)
    if invalid:
        # Returns the invalid error message and status code
        return invalid

    new_rental = Rental(customer_id=request_body["customer_id"],
                    video_id=request_body["video_id"],
                    due_date=create_due_date(request_body["phone"]),
    )

    db.session.add(new_rental)
    db.session.commit()

    new_rental_response = new_rental.to_dict()

    # Calculate, then add to new_rental_response
    videos_checked_out_count = 
    # Number of videos checked out by this customer_id
    # Count all rentals where customer_id is current rental's customer_id

    available_inventory = 
    # Count all rentals where video_id is current video_id
    # Then subract from total_inventory for video with this video_id

    return jsonify(new_rental_response), 201



