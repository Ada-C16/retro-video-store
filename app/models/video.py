from app import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    # Many to many: only counts each customer once. Secondary joins the third table
    # backref - joins two tables
    renters = db.relationship('Customer', secondary='rental')
    # One to many. Counts for all videos currently checked out
    rentals = db.relationship('Rental')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory
        }
