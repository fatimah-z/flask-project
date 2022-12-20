from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))


class Car(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    objectId = db.Column(db.String(25), nullable=False)
    createdAt = db.Column(db.String(25), nullable=False)
    updatedAt = db.Column(db.String(25), nullable=False)
    year = db.Column(db.INTEGER, nullable=True)
    make = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(25), nullable=True)
