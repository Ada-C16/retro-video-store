from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    def customer_details(self):
        return {
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone
        }

    def update_attributes(self, request_body):
        self.name =request_body["name"]
        self.postal_code=request_body["postal_code"]
        self.phone=request_body["phone"]
