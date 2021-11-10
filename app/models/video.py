from app import db
from dataclasses import dataclass


class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime())
    total_inventory = db.Column(db.Integer)