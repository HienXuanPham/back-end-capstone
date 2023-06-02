from flask import Blueprint, request, jsonify, make_response, abort, session
from app import db
from app.models.user import User
from app.models.note import Note
from app.models.login import Login
from app.models.signup import Signup
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__, url_prefix="/users")
api_bp = Blueprint("", __name__, url_prefix="")

# Helper function
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f" id {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if model:
        return model
    abort(make_response({"message": f" {cls.__name__} {model_id} not found."}, 404))

def validate_request(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
        abort(make_response(jsonify({"message": f"Request body must include {e}"}), 400))
    return new_obj

def hash_password(password):
    return generate_password_hash(password)

#--- Log in ---#
@api_bp.route("/login", methods=["POST"])
def user_log_in():
    request_data = request.get_json()
    user_login = validate_request(Login, request_data)

    user_email = user_login.email
    user_password = user_login.password

    db_user = User.query.filter_by(email=user_email).first()

    if db_user and check_password_hash(db_user.password, user_password):
        session["user_id"] = db_user.user_id
        return jsonify({
            "message": "success",
            "user_id": f"{db_user.user_id}"
        })
    
    return jsonify({"message": "Your email or password is incorrect"})

#--- GET CURRENT USER ---#
@api_bp.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"})
    user = User.query.filter_by(user_id=user_id).first()
    return user.to_dict()

#--- Sign Up ---#
@api_bp.route("/signup", methods=["POST"])
def sign_up():
    request_data = request.get_json()
    user_sign_up = validate_request(Signup, request_data)

    user_email = user_sign_up.email

    db_user = User.query.filter_by(email=user_email).first()

    if db_user is not None:
        return jsonify({"message": f"{user_email} already existed."})

    if user_sign_up.password != user_sign_up.confirm_password:
        return jsonify({"message": "Password and Confirm Password fields must be exactly"})
    
    new_user = User(
        name=user_sign_up.name,
        email=user_email,
        password=hash_password(user_sign_up.password)
    )

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id

    return jsonify({"message": "success", "user": new_user.to_dict()}), 201

#--- Log Out ---#
@api_bp.route("/logout", methods=["POST"])
def log_out():
    session.pop("user_id")
    return "200"

#--- User routes ---#
@users_bp.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user_info = validate_model(User, user_id)
    
    return user_info.to_dict()

@users_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = validate_model(User, user_id)
    request_body = request.get_json()
    user.name = request_body["name"]
    user.email = request_body["email"]
    user.password = hash_password(request_body["password"])

    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(f"User {user_id} successfully updated."))

@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_model(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({"message": f"User {user_id} successfully deleted."}))

#----- Notes -----#
@users_bp.route("/<user_id>/notes", methods=["POST"])
def create_new_note(user_id):
    user = validate_model(User, user_id)
    note_data = request.get_json()
    note_data["user_id"] = user.user_id
    new_note = validate_request(Note, note_data)

    db.session.add(new_note)
    db.session.commit()

    return make_response(new_note.to_dict(), 201)


@users_bp.route("/<user_id>/notes", methods=["GET"])
def get_all_notes(user_id):
    user = validate_model(User, user_id)

    notes_response = []
    for note in user.notes:
        notes_response.append(note.to_dict())

    return make_response(jsonify(notes_response), 200)

@users_bp.route("/<user_id>/notes/<note_id>", methods=["GET"])
def get_one_note(user_id, note_id):
    user = validate_model(User, user_id)
    note = validate_model(Note, note_id)

    return make_response(jsonify(note.to_dict()), 200)


@users_bp.route("/<user_id>/notes/<note_id>", methods=["PUT"])
def update_note(user_id, note_id):
    user = validate_model(User, user_id)
    note = validate_model(Note, note_id)
    note_update_data = request.get_json()
    note.title = note_update_data["title"]
    note.journal = note_update_data["journal"]

    db.session.add(note)
    db.session.commit()

    return make_response(jsonify(note.to_dict()), 200)

@users_bp.route("/<user_id>/notes/<note_id>", methods=["DELETE"])
def delete_note_by_id(user_id, note_id):
    user = validate_model(User, user_id)
    note = validate_model(Note, note_id)

    db.session.delete(note)
    db.session.commit()

    return make_response(jsonify({"message": f"Note {note_id} successfully deleted."}))


