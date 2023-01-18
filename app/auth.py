from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, Response, session

from app import app


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return Response('token is missing', status=400)
        try:
            if token == str(session['token']):
                payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms="HS256")
            if token == str(session['refresh token']):
                payload = jwt.decode(token, app.config.get('REFRESH_KEY'), algorithms="HS256")
            if str(datetime.utcnow()) >= session['expiry'] and (token == str(session['token'])):
                return Response('Token expired.Please refresh', status=200)
            elif str(datetime.utcnow()) >= session['expiry'] and not session['logged in']:
                return Response('Signature expired. Please log in again.', status=401)
            elif token == str(session['token']):
                return payload
            elif str(datetime.utcnow()) >= session['expiry'] and token == str(session['refresh token']):
                payload = {
                    'expiration': str(datetime.utcnow() + timedelta(seconds=20)),
                    'user': payload['user']
                }
                auth_token = jwt.encode(
                    payload,
                    app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                )
                payload_refresh = {
                    'expiration': str(datetime.utcnow() + timedelta(seconds=60)),
                    'user': payload['user']
                }
                refresh_token = jwt.encode(
                    payload_refresh,
                    app.config.get('REFRESH_KEY'),
                    algorithm='HS256'
                )
                session['logged in'] = False
                session['token'] = auth_token
                session['refresh token'] = refresh_token
                session['expiry'] = payload_refresh['expiration']
                return {'auth-token': auth_token, 'refresh-token': refresh_token}
            else:
                raise jwt.InvalidTokenError
                # return 'Invalid token.1 Please log in again.'
        except jwt.InvalidTokenError:
            return Response('Invalid token. Please log in again.', status=400)
        except Exception as e:
            return e

    return decorated
