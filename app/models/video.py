from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, nullable=True)
    # customer_id = db.Column(db.Integer, db.ForeignKey(
    #     "customer.customer_id"), nullable=True)

    def to_dict(self):
        """converts task data to dictionary"""
        result = {"video_id": self.video_id,
                  "title": self.title,
                  "release_date": self.release_date,
                  "total_inventory": self.total_inventory
                  }

        # if self.customer_id:
        #     result["customer_id"] = self.customer_id
        return result
