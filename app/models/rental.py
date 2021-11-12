from app import db
from app.models.customer import Customer
from app.models.customer import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    date_due = db.Column(db.DateTime)
    checked_in = db.Column(db.Boolean, default=False)

    def get_customer(self):
        customer = Customer.query.get(self.customer_id)
        return {
            "due_date": self.date_due,
            "name": customer.name,
            "phone":customer.phone,
            "postal_code": customer.postal_code
        }

    def get_video(self):
        video = Video.query.get(self.video_id)
        return {
            "due_date": self.date_due,
            "title": video.title,
            "release_date": video.release_date
        }