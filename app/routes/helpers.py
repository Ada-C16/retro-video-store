from app.models.customer import Customer 
from app.models.video import Video 
from flask import request

# helper methods for validation 
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
