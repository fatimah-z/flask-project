from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import request
from flask_login import login_user
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '12345678'
db = SQLAlchemy(app)
# db.init_app(app)

app.app_context().push()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)

@app.route('/')
def index():
    return "hello world"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user and check_password_hash(user.password,password):
        return "Incorrect Credentials"

    # login_user(user)
    return "Success"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        return "User already exists"

    new_user = User(email=email,password=generate_password_hash(password=password))
    db.session.add(new_user)
    db.session.commit()

    return "Success"

if __name__ == "__main__":
    app.run(debug=True)