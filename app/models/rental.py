from app import db


class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_ket=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_in = db.Column(db.Boolean, default=False)

    