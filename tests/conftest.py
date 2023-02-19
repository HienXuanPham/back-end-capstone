import pytest
from app import create_app, db
from flask.signals import request_finished
from app.models.user import User
from app.models.note import Note

USER_NAME = "Chelsea Pham"
PASSWORD = "journalstock123;"
NOTE_TITLE = "TSLA 2/10/23"
NOTE_MESSAGE = "Evening star on the daily"

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def one_saved_user(app):
    new_user = User(
        name = USER_NAME,
        password = PASSWORD
    )

    db.session.add(new_user)
    db.session.commit()

@pytest.fixture
def add_one_note_to_user_id_1(app, client):
    response = client.post("/users/1/notes", json = {
        "user_id": 1,
        "title": NOTE_TITLE,
        "journal": NOTE_MESSAGE
    })


