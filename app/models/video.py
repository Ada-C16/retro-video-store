from app import db

class Video(db.Model):
    __tablename__ = "videos_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
#    customers = db.relationship("Customer", secondary="rentals_table", backref="videos_table")

