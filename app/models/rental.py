from app import db

# join table 
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime()) 
    video = db.relationship('Video', backref='rentals')
    customer = db.relationship('Customer', backref='rentals')
