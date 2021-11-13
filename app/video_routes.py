from marshmallow import schema
from app import db
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import timedelta


video_bp = Blueprint("videos", __name__, url_prefix="/videos")
from app.models.video import PutVideoInputSchema
put_video_schema = PutVideoInputSchema()

@video_bp.route("", methods=["POST"])
def create_video():
    request_data=request.get_json()
    # not_field=put_video_schema.validate(request.form)
    if "title" not in request_data: 
        invalid_data={"details": "Request body must include title."}
        return jsonify(invalid_data),400
    elif "release_date" not in request_data:
        invalid_data={"details": "Request body must include release_date."}
        return jsonify(invalid_data),400
    elif "total_inventory" not in request_data:
        invalid_data={"details": "Request body must include total_inventory."}
        return jsonify(invalid_data),400
    
    new_video=Video(title=request_data["title"], release_date=request_data["release_date"], total_inventory=request_data["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos_response = []
    videos = Video.query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200



@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404
  
    return jsonify({"title": video.title, "id": video.id, "total_inventory": video.total_inventory}), 200
    

@video_bp.route("/<id>", methods=["PUT"])
def put_one_video(id): 
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404   
    request_data=request.get_json()
    errors = put_video_schema.validate(request_data)
    if errors:
        return jsonify({"details": f"{errors} Invalid data"}),400
    else:
        video.title=request_data["title"]
        video.release_date=request_data["release_date"]
        video.total_inventory=request_data["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()),200

@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    id=validate_id_int(id)
    
    video = Video.query.get(id)

    if video:
        if video.rentals:
            for rented_video in video.rentals:
                db.session.delete(rented_video)
                db.session.commit()
            return make_response("",200)
        db.session.delete(video)
        db.session.commit()
        return {"id": video.id}, 200
    else:
        return {"message":f"Video {id} was not found"}, 404

def validate_id_int(id):
    try:
        id = int(id)
        return (id)
    except:
        abort(400, "Error: id needs to be a number")

@video_bp.route("<video_id>/rentals", methods=["GET"])
def get_all_videos_rented(video_id):
    target_video_id=int(video_id)
    video_rented = Video.query.get(target_video_id)
    if not video_rented:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    # videos=video_rented.rentals
    customer_list=[]
    for cust in video_rented.rentals:
        customer_list.append({
            "due_date": cust.due_date,
            "name":cust.customer.name,
            "phone": cust.customer.phone,
            "postal_code": cust.customer.postal_code
            })
    return jsonify(customer_list), 200        

#*************************************************ENHANCEMENTS************************************************
@video_bp.route("/<id>/history", methods=["GET"])
def get_video_history(id):
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404
    video_history=[]
    for video in video.rentals:
        video_history.append({
        "customer_id": video.customer_id, 
        "name": video.customer.name,
        "postal_code": video.customer.postal_code, 
        "checkout_date": video.due_date-timedelta(days=7),
        "due_date": video.due_date })

    return jsonify(video_history), 200
