from app import db
from datetime import timedelta, date

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)