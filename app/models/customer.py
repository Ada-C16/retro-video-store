from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code
        }

    # def updated_dict(self):
    #     customer_dict = self.to_dict()
    #     for key in customer_dict:
    #         if key in ["name", "phone", "postal_code"]:
    #             customer_dict[key] = f"Updated ${customer_dict[key]}"
    #     return customer_dict

    def updated_dict(self):
        return {
            "id": self.id,
            "name": f"Updated ${self.name}",
            "phone": f"Updated ${self.phone}",
            "postal_code": f"Updated ${self.postal_code}"
        }
