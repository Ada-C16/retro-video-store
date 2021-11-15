from flask import jsonify

def check_valid_id(Obj, id):
    if type(id) == int:
        obj = Obj.query.get(id)
        return obj
    else:
        return "Invalid"

def not_found_message(Obj, id):
    return jsonify({"message": f"{Obj} {id} was not found"}), 404