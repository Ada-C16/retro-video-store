from app.models.customer import Customer 
from app.models.video import Video 
from flask import request

# helper methods for validation/error-checking 
def id_is_valid(id, object_type):
    '''
    returns two values: an object and None (if no error is present),
    or an "invalid" string and an error (if error is present) 
    '''
    if not id.isnumeric(): 
        return "invalid", ("", 400) 
    
    if object_type == "customer":
        object = Customer.query.get(id) 
    elif object_type == "video":
        object = Video.query.get(id)

    name = object_type.capitalize()
    if not object:
        return "invalid", ({"message": f"{name} {id} was not found"}, 404)  
    return object, None 

def request_has_all_required_categories(object_type):
    '''
    returns two values: request data in json format and None 
    (if no error is present), or an "invalid" string and an error message 
    (if error is present)
    '''
    request_data = request.get_json()

    required_categories = {
        "customer" : ["name", "phone", "postal_code"],
        "video" : ["total_inventory", "release_date", "title"],
        "rental" : ["customer_id", "video_id"]
    }

    for category in required_categories[object_type]:
        if category not in request_data: 
            return "invalid", (
                {"details" : f"Request body must include {category}."}, 400)
    return request_data, None 

def check_rental_errors():
    '''
    returns three values: a null value, a video_id and a customer_id 
    (if no error is present), or an error message and two null values 
    (if error is present)
    '''
    request_data, error_msg = request_has_all_required_categories("rental")
    if error_msg is not None:
        return error_msg, None, None   

    video_id = request_data["video_id"]
    _, error_msg = id_is_valid(str(video_id), "video")
    if error_msg is not None:
        return error_msg, None, None   
    
    customer_id = request_data["customer_id"]
    _, error_msg = id_is_valid(str(customer_id), "customer")
    if error_msg is not None:
        return error_msg, None, None  
    
    return None, video_id, customer_id 

# helper method for sorting + limiting results based on optional query params
def sort_limit_and_paginate(object):
    '''
    returns a list of either videos or customers that have been sorted 
    (if a sort query is present), limited (if a page limit query is present), 
    and paginated (if a pagination query is present); if no queries are present, 
    returns all videos or all customers in DB
    '''
    sort_query = request.args.get("sort")
    page_limit = request.args.get("n")
    pagination_query = request.args.get("p")

    possible_sort_queries = []
    if type(object) == Video:
        possible_sort_queries = ["title", "release_date"]
    elif type(object) == Customer:
        possible_sort_queries = ["name", "phone", "postal_code"]

    if not sort_query or sort_query not in possible_sort_queries:
        if pagination_query:
            objects = object.query.paginate(
                page=int(pagination_query),
                per_page=int(page_limit),error_out=False).items
        else:
            objects = object.query.limit(page_limit)
    elif sort_query in possible_sort_queries: 
        if pagination_query:
            objects = object.query.order_by(sort_query).paginate(
                page=int(pagination_query),
                per_page=int(page_limit),error_out=False).items
        else:
            objects = object.query.order_by(sort_query).limit(page_limit)
    else:
        objects = object.query.limit(page_limit)
    
    return objects 