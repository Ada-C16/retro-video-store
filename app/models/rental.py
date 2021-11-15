from app import db

class Rental(db.Model):
    __tablename__ = "rentals_table"
    # id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers_table.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos_table.id'),  primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime)