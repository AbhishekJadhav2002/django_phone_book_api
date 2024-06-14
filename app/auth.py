from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import db, User
from app import limiter, csrf


bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
@csrf.exempt
def register():
    data = request.get_json()
    name = data["name"]
    phone_number = data["phone_number"]
    password = data["password"]
    email = data.get("email")

    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({"message": "Phone number already registered"}), 400

    user = User(name=name, phone_number=phone_number, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    phone_number = data["phone_number"]
    password = data["password"]

    user = User.query.filter_by(phone_number=phone_number).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
