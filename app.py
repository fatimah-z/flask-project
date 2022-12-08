from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import request
from flask_login import login_user
from werkzeug.security import generate_password_hash,check_password_hash
from  celery import Celery
import requests
import json
import urllib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '12345678'
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


app.app_context().push()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objectId =  db.Column(db.String(25),nullable=False)
    createdAt = db.Column(db.String(25),nullable=False)
    updatedAt = db.Column(db.String(25),nullable=False)
    year = db.Column(db.INTEGER,nullable=True)
    make = db.Column(db.String(20),nullable=True)
    category = db.Column(db.String(25),nullable=True)


@app.route('/')
def index():
    return "hello world"

#Login Route
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

#signup route
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


@app.route('/getData',methods=['GET'])
def getdata():     
    result=syncdata()
    return result

@celery.task
def syncdata():
    url = 'https://parseapi.back4app.com/classes/Car_Model_List?count=1&limit=100'
    headers = {
        'X-Parse-Application-Id':'gP38fEGPgSSBvvO4Kz9McQD2UpUrcpIlrXDyHLWc',
        'X-Parse-REST-API-Key': '72gJMaTFClPr90oA7bkRYdUy0PJIcKQ8tj8bQvtP'
    }
    data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) 
    for record in data['results']:
        print('record',record)
        new_record = Car(objectId= record['objectId'],
                        createdAt=record['createdAt'],
                        updatedAt=record['updatedAt'],
                        year=None,
                        make =None,
                        category =None
                        # year=record['year'],
                        # make =record['make'],
                        # category = record['category']
                        )
        db.session.add(new_record)
    db.session.commit()
    
    return 'success'    

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)