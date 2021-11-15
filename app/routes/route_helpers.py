from flask import make_response, jsonify
def invalid_id(id):
    if not id.isnumeric():
            response_body = {
                'details': 'Invalid video id'
            }
            return make_response(jsonify(response_body), 400)
    return None