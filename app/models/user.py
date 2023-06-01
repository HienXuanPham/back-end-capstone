from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    notes = db.relationship("Note", back_populates="user")
    login = db.relationship("Login", backref="User", uselist=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "notes": [note.to_dict() for note in self.notes]
        }

    @classmethod
    def from_dict(cls, request_data):
        new_user = User(
            name = request_data["name"],
            email = request_data["email"],
            password = request_data["password"]
        )
        return new_user