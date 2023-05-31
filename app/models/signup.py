from app import db

class Signup(db.Model):
    signup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    confirm_password = db.Column(db.Text, nullable=False)

    @classmethod
    def from_dict(cls, request_data):
        new_signup = Signup(
            name = request_data["name"],
            email = request_data["email"],
            password = request_data["password"],
            confirm_password = request_data["confirm_password"]
        )
        return new_signup