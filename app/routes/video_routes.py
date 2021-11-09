
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request

# customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

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
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            })

        return jsonify(videos_response), 200


    elif request.method == "POST":
        request_body = request.get_json()
        #added these as conditionals instead of a combined one because they want
        # specific repsonse bodies for what was not included
        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        elif "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        elif "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400

        new_video = Video(title=request_body["title"], total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"])

        db.session.add(new_video)
        db.session.commit()
        #for some reason this test asks for the dict to be returned instead of the id
        new_video_dict = {
                "id": new_video.video_id,
                "title": new_video.title,
                "release_date": new_video.release_date,
                "total_inventory": new_video.total_inventory
            }
        return new_video_dict, 201

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_video(video_id):
    #added lines 63,64 for catching incorrect input type
    if video_id.isdigit() == False:
        return jsonify(None), 400
    
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"message": f"Video {video_id} was not found"}, 404)

    if request.method == "GET":
        # if video.goal_id:
        #     return {
        #     "task": {
        #         "id": video.id,
        #         "goal_id": task.goal_id,
        #         "title": task.title,
        #         "description": task.description,
        #         "is_complete": task.completed_at != None  
        #         }
        #     }
        # else:
        return jsonify({
            
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory   
                
            }), 200
    
    elif request.method == "PUT":
        request_body = request.get_json()
        #added these as conditionals instead of a combined one because they want
        # specific repsonse bodies for what was not included
        if "title" not in request_body:
            return jsonify({"details": "Request body must include title."}), 400
        elif "release_date" not in request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        elif "total_inventory" not in request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400

        #add code for edge case where inputs all there but one or more=invalid, for example toatal inventory is not an integer

# "The API should return back a 400 Bad Request response for missing or invalid fields in the request body.
# For example, if total_inventory is missing or is not a number"

        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]

        db.session.commit()

        return jsonify({
        
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory  
            
        })

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        #changed format of this based on test, it was asking for a key "id" and not an error message
        return jsonify({
            "id": video.video_id
            })


