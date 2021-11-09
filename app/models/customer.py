from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String) #I think this needs to be a string for the tests to pass
    phone = db.Column(db.String)
    registration_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registration_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    @classmethod
    def is_data_valid(cls, dict):
        types = {
            "name": str,
            "postal_code": str,
            "phone": str
        }
        for input_type in types:
            if not dict.get(input_type):
                return False, {"details": f"Request body must include {input_type}."}
            if type(dict.get(input_type)) != types[input_type]:
                return False, {"details": "invalid data"}
        return True, {"details": "valid data"}

    @classmethod
    def from_json(cls, dict):
        return Customer(name=dict["name"], postal_code=dict["postal_code"], phone=dict["phone"])

    @classmethod
    def is_int(cls, input):
        try:
            x = int(input)
        except ValueError:
            return False
        return True
