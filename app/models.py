import uuid

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __int__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    objectId = db.Column(db.String(25), nullable=False)
    createdAt = db.Column(db.String(25), nullable=False)
    updatedAt = db.Column(db.String(25), nullable=False)
    year = db.Column(db.INTEGER, nullable=True)
    make = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(25), nullable=True)

    def __init__(self, objectId, createdAt, updatedAt, year, make, category):
        self.id = str(uuid.uuid4())
        self.objectId = objectId
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.year = year
        self.make = make
        self.category = category
