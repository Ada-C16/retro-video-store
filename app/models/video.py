from enum import unique
from app import db
from flask import current_app


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, nullable=True)
