from app.models.customer import Customer 
from app.models.video import Video 
from flask import request

CUSTOMER_REQUIRED_CATEGORIES = ["name", "phone", "postal_code"]
VIDEO_REQUIRED_CATEGORIES = ["total_inventory", "release_date", "title"]

# helper methods for validation 
def id_is_valid(id, object_type):
    '''
    returns two values: an object or "invalid", plus an error message; 
    if no error is present, the error message is None
    '''
    if not id.isnumeric(): 
        return "invalid", ("", 400)
    
    if object_type == "customer":
        customer = Customer.query.get(id) 
        if not customer:
            return "invalid", ({"message": 
                                f"Customer {id} was not found"}, 
                                404)  

        # no error was caught; the id is valid 
        return customer, None 

def request_has_all_required_categories(object_type):
    '''
    returns two values: request data in json format, and an error message;
    if no error is present, the error message is None 
    '''
    request_data = request.get_json()

    if object_type == "customer":
        for required_category in CUSTOMER_REQUIRED_CATEGORIES:
            if required_category not in request_data: 
                return request_data, ({"details" : 
                        f"Request body must include {required_category}."}, 
                        400)

        # no error was caught; all required categories are present 
        return request_data, None  