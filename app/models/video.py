from app import db
from app.models.rental import Rental

class Video(db.Model):
    # building the database table with columns, data type, column names
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime) #should this be nullable?
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, nullable = True)
    customers = db.relationship("Rental", backref='Video', cascade="all, delete-orphan", lazy="joined")

    def video_checked_out_count(self):
        rental_query = Rental.query.filter_by(video_id=self.id, checked_in=False)
        return rental_query.count()

    def available_inventory(self):
        available_inv = self.total_inventory - self.video_checked_out_count()
        return available_inv

