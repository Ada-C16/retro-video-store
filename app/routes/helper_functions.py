from flask import make_response, abort
from app.models.video import Video
from app.models.customer import Customer

# HELPER FUNCTIONS
def validate_id(id, id_type):
    try:
        int(id)
    except:
        abort(make_response({"error": f"{id_type} must be an int"}, 400))

def get_video_from_id(id):
    validate_id(id, 'video id')
    selected_video = Video.query.get(id)
    if not selected_video:
        abort(make_response({'message': f'Video {id} was not found'}, 404))
    return selected_video

def get_customer_data_with_id(customer_id):
    validate_id(customer_id, "id")
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

    return customer

def confirm_all_video_fields_present(request_body):
    missing_fields = []
    if 'title' not in request_body:
        missing_fields.append('Request body must include title.')
    if 'release_date' not in request_body:
        missing_fields.append('Request body must include release_date.')
    if 'total_inventory' not in request_body:
        missing_fields.append('Request body must include total_inventory.')
    if missing_fields:
        abort(make_response({'details': missing_fields}, 400))