from app import db

class Login(db.Model):
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    @classmethod
    def from_dict(cls, request_data):
        new_login = Login(
            email = request_data["email"],
            password = request_data["password"]
        )
        return new_login