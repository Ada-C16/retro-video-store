from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # datetime.datetime.now(datetime.timezone.utc)