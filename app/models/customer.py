from sqlalchemy.sql.functions import func
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def customer_dict(self):
        return {
            "id": self.task_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "register_at": self.register_at.strftime("%a, %d %b %Y %X %z")
        }
