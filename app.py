from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import request
from flask_login import login_user
from werkzeug.security import generate_password_hash,check_password_hash
from  celery import Celery
import requests
import json
import schedule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '12345678'
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL']) #celery configuration
celery.conf.update(app.config)


#user model for user credentials
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(20),nullable=False)

#car model for car registrations
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objectId =  db.Column(db.String(25),nullable=False)
    createdAt = db.Column(db.String(25),nullable=False)
    updatedAt = db.Column(db.String(25),nullable=False)
    year = db.Column(db.INTEGER,nullable=True)
    make = db.Column(db.String(20),nullable=True)
    category = db.Column(db.String(25),nullable=True)


#signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() #Retreiving the json data
    email = data["email"]   #Retreiving the email value
    password = data["password"] #Retreiving the password value

    user = User.query.filter_by(email=email).first() #Query the db 
                                                    #to check if email already exists
    #if user exists
    if user:
        return "User already exists"

    #if users does not exists create new
    new_user = User(email=email,password=generate_password_hash(password=password))
    db.session.add(new_user) #adding record to db session
    db.session.commit() #committing changes to db session

    return "Success"

#Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() #Retreiving the json data
    email = data["email"] #Retreiving the email value
    password = data["password"] #Retreiving the password value

    user = User.query.filter_by(email=email).first() #Query the db 
                                                    #to check if email already exists

    if not user and check_password_hash(user.password,password):
        return "Incorrect Credentials"

    return "Success"

@app.route('/getData',methods=['GET'])
def getdata():     
    result=syncdata() #calling the method as background task
    return result

@celery.task
def syncdata():
    url = 'https://parseapi.back4app.com/classes/Car_Model_List?count=1&limit=100'
    headers = {
        'X-Parse-Application-Id':'gP38fEGPgSSBvvO4Kz9McQD2UpUrcpIlrXDyHLWc',
        'X-Parse-REST-API-Key': '72gJMaTFClPr90oA7bkRYdUy0PJIcKQ8tj8bQvtP'
    }
    data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))

    #traversing our each object in the results array 
    for record in data['results']:
        existing = Car.query.filter_by(objectId=record['objectId']).first()
        #if record does not exist create new
        if(existing == None): 
            new_record = Car(objectId= record['objectId'],
                            createdAt=record['createdAt'],
                            updatedAt=record['updatedAt'],
                            year=None, #data fetched has missing attributes
                            make =None,
                            category =None
                            # year=record['year'],
                            # make =record['make'],
                            # category = record['category']
                            )

            db.session.add(new_record)
        #if changes found in existing record update it
        elif(existing.__dict__ != record):
            print('in update')
            existing.createdAt = record['createdAt']
            existing.updatedAt = record['updatedAt']
            existing.year = None
            existing.make = None
            existing.category = None
            # existing.year = record['year']
            # existing.make = record['make']
            # existing.category = record['catgory']


    db.session.commit()
    
    return 'success'    


schedule.every().day.at('00:00').do(syncdata) #tried implementing automated call to updata data


with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug=True)