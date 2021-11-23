from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date(), nullable=True)
    total_inventory = db.Column(db.Integer(), nullable=False)
    # relationship
    customers = db.relationship("Customer", secondary="rental", backref="video",lazy=True)


    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory" :  self.total_inventory
        }

