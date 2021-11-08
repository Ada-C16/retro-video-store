
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

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

        return jsonify(tasks_response), 200


    elif request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body or "total_inventory" not in request_body:

            return jsonify({
                "details": "Invalid data"
            }), 400

        new_video = Video(title=request_body["title"], total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"])

        db.session.add(new_video)
        db.session.commit()
       
       #START AGAIN HEREEEEE
        # return jsonify(
        #     {
        #         "task": {
        #         "id": new_task.task_id,
        #         "title": new_task.title,
        #         "description": new_task.description,
        #         "is_complete": new_task.completed_at != None  
        #         }
        #     }), 201

# @tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
# def handle_task(task_id):
#     task = Task.query.get(task_id)

#     if task is None:
#         return make_response(f"Task {task_id} not found", 404)

#     if request.method == "GET":
#         if task.goal_id:
#             return {
#             "task": {
#                 "id": task.task_id,
#                 "goal_id": task.goal_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": task.completed_at != None  
#                 }
#             }
#         else:
#             return {
#                 "task": {
#                     "id": task.task_id,
#                     "title": task.title,
#                     "description": task.description,
#                     "is_complete": task.completed_at != None  
#                     }
#                 }
    
#     elif request.method == "PUT":
#         form_data = request.get_json()

#         task.title = form_data["title"]
#         task.description = form_data["description"]

#         db.session.commit()

#         return jsonify({
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.completed_at != None  
#             }
#         })

#     elif request.method == "DELETE":
#         db.session.delete(task)
#         db.session.commit()
#         return jsonify({
#         "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
#         })


# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def handle_mark_complete(task_id):
#     task = Task.query.get(task_id)

#     if task is None:
#         return make_response(f"Task {task_id} not found", 404)
    
#     if request.method == "PATCH":
#         task.completed_at = datetime.now()
        
#         db.session.commit()

#         SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

#         header={"Authorization": SLACK_API_KEY} 

#         path = "https://slack.com/api/chat.postMessage"

#         query_params= {
#             "channel": "slack-api-test-channel",
#             "text": f"Someone just completed the task {task.title}"
#         }

#         requests.post(path, data=query_params, headers=header)  

#         return jsonify({
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.completed_at != None
#             }
#         })

# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def handle_mark_incomplete(task_id):
#     task = Task.query.get(task_id)

#     if task is None:
#         return make_response(f"Task {task_id} not found", 404)
    
#     if request.method == "PATCH":
#         task.completed_at = None
        
#         db.session.commit()

#         return jsonify({
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.completed_at != None
#             }
#         })
