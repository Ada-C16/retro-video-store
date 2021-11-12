
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


#issue with abort
#STILL NEED TO CHECK DATATYPES

def check_for_input(request_body, list_of_attributes):
   
    for attribute in list_of_attributes:
        if attribute not in request_body:
            error_message = jsonify({"details": f"Request body must include {attribute}."})

            abort(400, error_message)
            
     
 


@videos_bp.route("", methods=["GET", "POST"])
def handle_videos():
    
    if request.method == "GET":
        sort_query = request.args.get("sort")
        
        if sort_query == "asc":
            videos = Video.query.order_by(Video.title.asc())
        
        elif sort_query == "desc":
            videos = Video.query.order_by(Video.title.desc())
            
        else:
            videos = Video.query.all()

        videos_response = []
        for video in videos:
            video_dict = video.to_dict()
            videos_response.append(video_dict)

        return jsonify(videos_response), 200


    elif request.method == "POST":
        request_body = request.get_json()
        
        list_of_attributes = ["title", "total_inventory", "release_date"]

        # for attribute in list_of_attributes:
        #     if attribute not in request_body:
        #         error_message = jsonify({"details": f"Request body must include {attribute}."})

        #         return error_message, 400

        check_for_input(request_body,list_of_attributes)
        #NEED TO ADD
        # check for correct type of input
        # (type("name") is not str)
        # (type("postal_code") is not str)
        # (type("phone") is not str)

        #refactor to make one return statement
            # return jsonify({"details": "Request body must include release_date."}), 400
        # 

        # if "title" not in request_body:
        #     return jsonify({"details": "Request body must include title."}), 400
        # elif "release_date" not in request_body:
        #     return jsonify({"details": "Request body must include release_date."}), 400
        # elif "total_inventory" not in request_body:
        #     return jsonify({"details": "Request body must include total_inventory."}), 400

        new_video = Video(title=request_body["title"], total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"])

        db.session.add(new_video)
        db.session.commit()
        
        new_video_dict = new_video.to_dict()

        return jsonify(new_video_dict), 201

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_video(video_id):
    if video_id.isdigit() == False:
        return jsonify(None), 400
    
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"message": f"Video {video_id} was not found"}, 404)

    if request.method == "GET":

        video_dict = video.to_dict()

        return jsonify(video_dict), 200
    
    elif request.method == "PUT":
        request_body = request.get_json()

        list_of_attributes = ["title", "total_inventory", "release_date"]

        check_for_input(request_body, list_of_attributes)

        #NEED TO ADD
        # check for correct type of input
        # (type("name") is not str)
        # (type("postal_code") is not str)
        # (type("phone") is not str)

        # if "title" not in request_body:
        #     return jsonify({"details": "Request body must include title."}), 400
        # elif "release_date" not in request_body:
        #     return jsonify({"details": "Request body must include release_date."}), 400
        # elif "total_inventory" not in request_body:
        #     return jsonify({"details": "Request body must include total_inventory."}), 400

        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

        db.session.commit()

        video_dict = video.to_dict()

        return jsonify(video_dict), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id": video.id
            })


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_customers_with_video_rented(video_id):
    if video_id.isdigit() == False:
        return jsonify(None), 400

    video = Video.query.get(video_id)
    if video is None:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    
    rentals = Rental.query.filter_by(video_id=video_id, checked_in=False)

    response_body = []

    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        response_body.append({
        "due_date": rental.due_date,
        "name": customer.name,
        "phone": customer.phone,
        "postal_code": customer.postal_code
    })

    return jsonify(response_body), 200

    