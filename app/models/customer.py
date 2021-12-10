from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos = db.relationship("Video", secondary="rental", backref="customer")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    def rental_dict(self, rental):
        return {
            "due_date": rental.due_date,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code}