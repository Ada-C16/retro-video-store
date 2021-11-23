from flask import make_response, jsonify
def invalid_id(id):
    if not id.isnumeric():
            response_body = {
                'details': 'Invalid video id'
            }
            return make_response(jsonify(response_body), 400)
    return None

def invalid_request_body(request_body, required_keys):
    for key in required_keys:
        if key not in request_body:
            response_body = {
                'details': f'Request body must include {key}.'
            }
            return make_response(response_body, 400)
    return None