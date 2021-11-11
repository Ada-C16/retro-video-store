from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey(
        'video.id'), nullable=True)
    # checkout_date = db.Column(db.DateTime, nullable=True)


    def to_dict(self, videos_checked_out_count, available_inventory):
        return {
            "customer_id": self.customer_id,
            "video_id": self.customer_id,
            # "due_date":
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory":available_inventory,
                }
