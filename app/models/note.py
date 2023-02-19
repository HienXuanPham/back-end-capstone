from app import db
from sqlalchemy.orm import relationship

class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    journal = db.Column(db.Text)
    user = db.relationship("User", back_populates="notes")
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def to_dict(self):
        note_dict = {
            "note_id": self.note_id,
            "user_id": self.user_id,
            "title": self.title,
            "journal": self.journal
        }
        return note_dict

    @classmethod
    def from_dict(cls, note_data):
        new_note = Note(
            user_id = note_data["user_id"],
            title = note_data["title"],
            journal = note_data["journal"]
        )
        return new_note