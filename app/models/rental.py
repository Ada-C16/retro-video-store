from app import db
"""
A Customer can have many Videos through a secondary table (i.e. Rentals), and a Video can be checked out/in by many Customers through the same Rentals table.
"""
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)