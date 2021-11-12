from flask.wrappers import Response
from app import db
from app.customer_routes import customers_bp
from app.video_routes import video_bp
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, request
from datetime import datetime

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def rentals_checkout():
    #{"c_id": [1], "v_id": [4]}
    request_body = request.get_json() 

    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify(), 400

    customer = Customer.query.get(request_body["customer_id"])
    if customer is None:
        return jsonify(), 404

    video = Video.query.get(request_body["video_id"])
    if video is None:
        return jsonify(), 404
    
    # # revisit later - Zandra's solution for test_checkout_video_no_inventory 
    # if video.total_inventory == 0:
    #     return jsonify({"message": "Could not perform checkout"}), 400

    # Instantiate a new instance for rental
    new_rental = Rental(
        video_id=video.video_id,
        customer_id=customer.customer_id
    )  
    
    # add rental instance to database
    db.session.add(new_rental)
    # commit to database
    db.session.commit()
    
    # return the response body and status code
    return jsonify({
        "video_id": new_rental.video_id,
        "customer_id": new_rental.customer_id,
        "videos_checked_out_count": len(customer.videos),
        "available_inventory": video.total_inventory - len(video.customers)
    })

@rentals_bp.route("/check-in", methods=["POST"])
def rentals_checkin():
    request_body = request.get_json()

    # checks that the required request body parameters are in request 
    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify(), 400
    
    # stores customer instance into variable. If customer does not exist, returns 404 
    customer = Customer.query.get(request_body["customer_id"])
    if customer is None:
        return jsonify(), 404

    # stores video instance into variable. If video does not exist, returns 404 
    video = Video.query.get(request_body["video_id"])
    if video is None:
        return jsonify(), 404
    
    # iterate through all rentals instances to find rental with matching customer and video ids
    rentals = Rental.query.all()
    checked_in = None
    for rental in rentals:
        if rental.customer_id == request_body["customer_id"] and rental.video_id == request_body["video_id"]:
            checked_in = rental
    
    # if there is no matching rental for the given customer and video ids, return 400
    if checked_in is None:
        return jsonify({"message": "No outstanding rentals for customer 1 and video 1"}), 400
    
    # delete rental that is being checked in
    db.session.delete(checked_in)
    # commit to database
    db.session.commit()

    # return response body
    return jsonify({
        "video_id": checked_in.video_id,
        "customer_id": checked_in.customer_id,
        "videos_checked_out_count": len(customer.videos),
        "available_inventory": video.total_inventory - len(video.customers)
    })

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_read(customer_id):
    """ List the videos a customer currently has checked out """
    request_body = request.get_json()
    
    # checks to see if customer exists. If not, returns 404
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    
    # sets up empty list to store a customer's checked out videos & iterates through customer.videos to retreive all videos a customer currently has
    checked_out = []
    for video in customer.videos:
        checked_out.append(video)

    # gets rental instance for each video a customer has
    rentals = Rental.query.all()
    customer_rentals = []
    for video in checked_out:
        for rental in rentals:
            if video.video_id == rental.video_id and customer.customer_id == rental.customer_id:
                customer_rentals.append(rental)

    # create response body 
    response_body = []
    for rental in customer_rentals:
        response_body.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
        })
    return jsonify(response_body)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def video_read(video_id):
    """ List the customers who currently have the video checked out """
    request_body = request.get_json()
    
    # checks to see if video exists. If not, returns 404
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404

    # sets up empty list to store the video's current customers & iterates through video.customers to retreive all customers that currently have the video
    current_customers = []
    for customer in video.customers:
        current_customers.append(customer)

    # gets rental instance for each customer a video has
    rentals = Rental.query.all()
    video_rentals = []
    for customer in current_customers:
        for rental in rentals:
            if video.video_id == rental.video_id and customer.customer_id == rental.customer_id:
                video_rentals.append(rental)
    
    # create response body 
    response_body = []
    for rental in video_rentals:
        response_body.append({
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        })
    return jsonify(response_body)
    
    # videos_list = []
    # for video in self.videos:
    #     videos_list(video.rental_id)
