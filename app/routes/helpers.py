from app.models.customer import Customer 
from app.models.video import Video 
from flask import request

# helper methods for validation 
def id_is_valid(id, object_type):
    '''
    returns two values: an object and None (if no error is present),
    or an "invalid" string and an error (if error is present) 
    '''
    if not id.isnumeric(): # /rentals/
        return "invalid", ("", 400) 
    
    if object_type == "customer":
        object = Customer.query.get(id) 
    elif object_type == "video":
        object = Video.query.get(id)

    name = object_type.capitalize()
    if not object:
        return object, ({"message": f"{name} {id} was not found"}, 404)  
    return object, None 

def request_has_all_required_categories(object_type):
    '''
    returns two values: request data in json format and None 
    (if no error is present), or the request data and an error message 
    (if error is present)
    '''
    request_data = request.get_json()

    if object_type == "customer":
        required_categories = ["name", "phone", "postal_code"]
    elif object_type == "video":
        required_categories = ["total_inventory", "release_date", "title"]
    elif object_type == "rental":
        required_categories = ["customer_id", "video_id"]

    for category in required_categories:
        if category not in request_data: 
            return request_data, (
                {"details" : f"Request body must include {category}."}, 400)
    return request_data, None 
