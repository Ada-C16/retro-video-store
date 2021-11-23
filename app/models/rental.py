from sqlalchemy.orm import relationship
from app import db
from app.models.customer import Customer
from app.models.video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)

    # videos_checked_out_count= db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer)
