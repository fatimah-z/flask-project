from datetime import datetime, timedelta

import jwt
from flask import json, request, Response, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.auth import token_required
from app.models import User


# route to check if jwt authentication is successful
@app.route('/home', methods=['GET'])
@token_required
def home(payload):
    return Response(json.dumps(payload), status=200)
    # return "Response('Authenticated', status=200)"


@app.route('/refresh-token', methods=['GET'])
@token_required
def refresh(payload):
    return Response(json.dumps(payload), status=200)


@app.route('/signup', methods=['POST'])
def signup():
    """
    This functions takes user credentials for authorization  and returns an HTTP response
    """
    data = request.get_json()  # Retrieving the json data
    user = User.query.filter_by(email=data.get('email')).first()  # Query the db
    # to check if email already exists

    if not user:
        try:
            user = User(
                email=data.get('email'),
                password=generate_password_hash(password=data.get('password'))
            )
            db.session.add(user)  # adding record to db session
            db.session.commit()  # committing changes to db session
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
            return Response(json.dumps(response_object), status=200)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return Response(json.dumps(response_object), status=401)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return Response(json.dumps(response_object), status=202)


# Login Route
@app.route('/login', methods=['POST'])
def login():
    """
        This functions takes user credentials for authentication and log in. It returns an HTTP response
    """
    data = request.get_json()  # Retrieving the json data
    # to check if email already exists

    try:
        user = User.query.filter_by(email=data.get('email')).first()  # Query the db
        payload = {
            'expiration': str(datetime.utcnow() + timedelta(seconds=20)),
            'user': user.id
        }
        auth_token = jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        payload_refresh = {
            'expiration': str(datetime.utcnow() + timedelta(seconds=30)),
            'user': user.id
        }
        refresh_token = jwt.encode(
            payload_refresh,
            app.config.get('REFRESH_KEY'),
            algorithm='HS256'
        )
        if user and check_password_hash(user.password, data.get('password')):
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token,
                    'refresh_token': refresh_token
                }
                session['logged in'] = True
                session['token'] = auth_token
                session['expiry'] = payload['expiration']
                session['refresh token'] = refresh_token
                return Response(json.dumps(response_object), status=200)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist'
            }
            return Response(json.dumps(response_object), 401)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return Response(json.dumps(response_object), status=401)

# @app.route('/fetchData', methods=['GET'])
# def fetch():
#     url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10'
#     headers = {
#         'X-Parse-Application-Id': 'WDMOU1Qwd4krcZ8ukdFzNcgwZQjckZr8iAn6REKG',
#         'X-Parse-REST-API-Key': 'FDbiA367WWEgIF7LEJjEfddu1sJ6rzykGR626EF8'
#     }
#
#     data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
#
#     try:
#         for item in data['results']:
#             existing_car = db.session.query(Car).filter_by(objectId=item['objectId']).first()
#
#             if not existing_car:
#                 car = Car(objectId=item['objectId'],
#                           createdAt=item['createdAt'],
#                           updatedAt=item['updatedAt'],
#                           year=item['Year'],
#                           make=item['Make'],
#                           category=item['Category']
#                           )
#                 db.session.add(car)
#                 db.session.commit()
#             else:
#                 if existing_car.year != item['Year']:
#                     existing_car.year = item['Year']
#                 if existing_car.make != item['Make']:
#                     existing_car.make = item['Make']
#                 if existing_car.category != item['Category']:
#                     existing_car.category = item['Category']
#                 if existing_car.updatedAt != item['updatedAt']:
#                     existing_car.updatedAt = item['updatedAt']
#                 if existing_car.updatedAt != item['createdAt']:
#                     existing_car.updatedAt = item['createdAt']
#                 db.session.commit()
#
#         response_object = {
#             'status': 'success',
#             'data': data
#         }
#         return Response(json.dumps(response_object), status=200)
#     except Exception as e:
#         response_object = {
#             'status': 'fail',
#             'message': str(e)
#         }
#         return Response(json.dumps(response_object), status=401)
