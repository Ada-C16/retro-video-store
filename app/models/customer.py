from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos = db.relationship("Video", secondary="rental", backref="customer")

    def to_dict(self):
        customer = {
            "id" : self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code
        }

        return customer

    #why do we need this decorator
    #why do we need to call Customer here and in routes
    @classmethod
    def from_dict(cls, request_body):
        customer = Customer(
            name=request_body["name"], 
            postal_code=request_body["postal_code"],
            phone=request_body["phone"]
        )
        return customer
