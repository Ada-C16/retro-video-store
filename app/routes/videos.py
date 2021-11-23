from app.models.video import Video
from app.models.rental import Rental 
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes.helper_functions import *

video_bp = Blueprint('video', __name__, url_prefix='/videos')

VIDEOS_PER_PAGE = 10


''' Post - create a new video'''
@video_bp.route("", methods=["POST"])
def add_video():
    request_body = request.get_json() 

    try:   
        new_video = Video(title = request_body["title"], 
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])
    except KeyError as err:
        response_body = {"details": f"Request body must include {err.args[0]}."}
        return make_response(response_body, 400) 
        
    db.session.add(new_video)
    db.session.commit()
    response_body = {"title": new_video.title,
                        "id": new_video.id,
                        "release_date": new_video.release_date,
                        "total_inventory": new_video.total_inventory}

    return make_response(jsonify(response_body),201)

'''Get - real all videos'''
@video_bp.route("", methods=["GET"])
def read_all():

    sort_videos = request.args.get("sort")
    page = request.args.get("page", 1, type=int) 
    # set default to 1, 
    # error_out will return an empty list when page > elements
    response_body = []

    if sort_videos == "title-asc":
        videos = Video.query.order_by(Video.title.asc()).paginate(page=page,per_page=VIDEOS_PER_PAGE,error_out=False)

    elif sort_videos == "release-date-asc":
        videos = Video.query.order_by(Video.release_date.asc()).paginate(page=page,per_page=VIDEOS_PER_PAGE,error_out=False)
    else:
        videos = Video.query.paginate(page=page, per_page=VIDEOS_PER_PAGE,error_out=False)
    
    for video in videos.items:
        response_body.append(video.to_json())     
    return make_response(jsonify(response_body),200)


'''GET - read one'''
@video_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = get_video_by_id(video_id)
    response_body = video.to_json()
    return make_response(jsonify(response_body),200)


''' PUT- update whole video row'''

@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id): 

    video = get_video_by_id(video_id)
    request_body = request.get_json()

    if not request_body or "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        response_body = {"message": "Invalid Data"}
        abort(make_response(response_body, 400))    

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()
    response_body = video.to_json()

    return make_response(response_body, 200)


'''DELETE - one item by id'''
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id): 
    video = get_video_by_id(video_id)
    rentals = Rental.query.filter_by(video_id=video_id).all()

    if rentals != None:
        for rental in rentals:
            db.session.delete(rental)
            db.session.commit()
    db.session.delete(video)
    db.session.commit()
    response_body ={"id": video.id}

    return make_response(response_body,200)


@video_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_video_id(id):

    get_video_by_id(id)
    rentals  = Rental.query.filter_by(video_id=id).all()
    response_body = []
    for rental in rentals:
        customer =  get_customer_from_id(rental.customer_id)
        response_body.append({"due_date": rental.due_date,
                            "name": customer.name,
                            "phone": customer.phone,
                            "postal_code":customer.postal_code})

    return make_response(jsonify(response_body),200)


@video_bp.route("/<id>/history", methods=["GET"])
def get_video_history(id):
    video = get_video_by_id(id)
    rentals  = Rental.query.filter(Rental.video_id==video.id, Rental.checked_in !=None).all()
    print(rentals)
    response_body =[]
    for rental in rentals:
        customer = get_customer_from_id(rental.customer_id)
        video = get_video_by_id(rental.video_id)
        response_body.append({"Customer name": customer.name,
                            "video": video.title,
                            "check-in date": rental.checked_in,
                            "video_id": rental.video_id,
                            "customer_id": rental.customer_id, 
                            "checkout date": rental.checkout_date})

    return make_response(jsonify(response_body), 200)

