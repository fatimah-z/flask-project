from flask import request, Response
from app.models import User
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Retrieving the json data
    email = data["email"]  # Retrieving the email value
    password = data["password"]  # Retrieving the password value

    user = User.query.filter_by(email=email).first()  # Query the db
    # to check if email already exists
    # if user exists
    if user:
        return Response("User Already exists", status=409)

    # if users does not exist create new
    new_user = User(email=email, password=generate_password_hash(password=password))
    db.session.add(new_user)  # adding record to db session
    db.session.commit()  # committing changes to db session

    return Response("Signup Success", status=201)


# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Retrieving the json data
    email = data["email"]  # Retrieving the email value
    password = data["password"]  # Retrieving the password value

    user = User.query.filter_by(email=email).first()  # Query the db
    # to check if email already exists

    if not user and check_password_hash(user.password, password):
        return Response("Incorrect Credentials", status=401)

    return Response("login success", status=200)

