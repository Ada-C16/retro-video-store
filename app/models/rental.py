from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = True, primary_key = True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable = True, primary_key = True)
    # due_date = db.Column(db.DateTime)
#     >>> import datetime
# >>> datetime.datetime.now() + datetime.timedelta(days=7)
