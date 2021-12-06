from app import db

class Rental(db.Model):
    __tablename__ = "rentals_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers_table.id'),nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos_table.id'),nullable=False)
    due_date = db.Column(db.DateTime)
    checked_in_status = db.Column(db.Boolean, default=False)