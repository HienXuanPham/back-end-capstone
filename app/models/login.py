from app import db

class Login(db.Model):
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    # def to_dict(self):
    #     return {
    #         "login_id": self.login_id,
    #         "email": self.email
    #     }

    @classmethod
    def from_dict(cls, request_data):
        new_login = Login(
            email = request_data["email"],
            password = request_data["password"]
        )
        return new_login