from app import db
from app.models.customer import Customer
from flask import  make_response, abort
from app.models.video import Video



def valid_int(number):
    try:
        id = int(number)
        return id 
    except:
        response_body = 'Invalid Data'
        abort(make_response(response_body,400))



def get_customer_from_id(customer_id):
    id = valid_int(customer_id)
    customer = Customer.query.filter_by(id=id).one_or_none()    
    if customer is None:
        response_body = {"message": f"Customer {id} was not found"}
        abort(make_response(response_body, 404))   
    return customer

def get_video_by_id(video_id):
    id = valid_int(video_id)
    video = Video.query.filter_by(id=id).one_or_none()    
    if video is None:
        response_body = {"message": f"Video {id} was not found"}
        abort(make_response(response_body, 404))   
    return video

def get_customer_and_video_id(request_body):
    customer = get_customer_from_id(request_body['customer_id'])
    video =  get_video_by_id(request_body['video_id'])
    return customer,video


def validate_request(action, request_body):
    if "customer_id" not in request_body or "video_id" not in request_body:
        return abort(make_response({"message": f"Could not perform {action}"}, 400))
