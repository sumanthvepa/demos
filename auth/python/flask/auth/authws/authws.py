import os
from enum import Enum
from http import HTTPStatus

import bcrypt
from werkzeug.exceptions import HTTPException
from flask import Flask, request


app = Flask(__name__)
app.secret_key = os.environ.get('AUTHWS_FLASK_SECRET_KEY')
if app.secret_key is None:
  raise RuntimeError(
    'AUTHWS_FLASK_SECRET_KEY must be set for the auth app to run')


class AuthStatus(Enum):
  def __new__(cls, *args, **kwds):
    value = len(cls.__members__) + 1
    obj = object.__new__(cls)
    obj._value = value
    return obj

  def __init__(self, error_code, http_status, description):
    super().__init__()
    self.error_code = error_code
    self.http_status = http_status
    self.description = description

  def to_tuple(self, additional_description=None):
    description = self.description
    if additional_description:
      description += ': ' + additional_description
    return tuple([{'error_code': self.error_code, 'error_message': description}, self.http_status])

  SUCCESS = 0, HTTPStatus.OK, 'Ok'
  NO_USERNAME_EMAIL_SUPPLIED = 1, HTTPStatus.BAD_REQUEST, 'Query parameter username_email not supplied'
  NO_SUCH_USER = 2, HTTPStatus.NOT_FOUND, 'No such user'
  NO_PASSWORD_SUPPLIED = 3, HTTPStatus.BAD_REQUEST, 'Query parameter password not supplied'
  INCORRECT_PASSWORD = 4, HTTPStatus.FORBIDDEN, 'Incorrect password'
  INVALID_APP_USER_TOKEN = 5, HTTPStatus.BAD_REQUEST, 'Invalid application user token'
  CLIENT_ERROR = 6, HTTPStatus.BAD_REQUEST, 'Client error'
  INTERNAL_ERROR = 7, HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal error'
  OTHER_ERROR = 8, HTTPStatus.INTERNAL_SERVER_ERROR, 'Other error'


class AuthError(RuntimeError):
  def __init__(self, status):
    super().__init__(status.description)
    self.status = status

  def to_tuple(self):
    return self.status.to_tuple()


@app.errorhandler(AuthError)
def handle_authentication_errors(ex):
  return ex.to_tuple()


@app.errorhandler(HTTPException)
def handle_http_exceptions(ex):
  auth_status = AuthStatus.OTHER_ERROR
  if 400 <= ex.code < 500:
    auth_status = AuthStatus.CLIENT_ERROR
  if ex.code >= 500:
    auth_status = AuthStatus.INTERNAL_ERROR
  return auth_status.to_tuple(str(ex))


@app.errorhandler(Exception)
def handle_errors(ex):
  return AuthStatus.INTERNAL_ERROR.to_tuple(str(ex))


# TODO: Move these dictionaries to authws and fetch them from the database
users = {
  '1': {
    'user_id': 1,
    'username': 'luser',
    'email': 'luser@example.com',
    'display_name': 'Lawrence Un Ser'
  }
}

password_hashes = {
  '1': bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt(12))
}

by_username = dict(zip([user['username'] for user in users.values()], users.values()))
by_email = dict(zip([user['email'] for user in users.values()], users.values()))


def find_user_by_username(username):
  return by_username.get(username, None)


def find_user_by_email(email):
  return by_email.get(email, None)


def find_user_by_username_or_email(username_email):
  from_username = find_user_by_username(username_email)
  from_email = find_user_by_email(username_email)
  user = from_username or from_email
  if not user:
    raise AuthError(AuthStatus.NO_SUCH_USER)
  return user


def user_from_user_id(user_id):
  user = users.get(str(user_id), None)
  if not user:
    raise AuthError(AuthStatus.NO_SUCH_USER)
  return user


@app.route('/api/users/', methods=['GET'])
def find_user():
  username_email = request.args.get('username_email')
  if not username_email:
    raise AuthError(AuthStatus.NO_USERNAME_EMAIL_SUPPLIED)
  return {'user_id': find_user_by_username_or_email(username_email)['user_id']}


@app.route('/api/user/<int:user_id>/authenticate', methods=['GET'])
def authenticate_user(user_id):
  user = user_from_user_id(user_id)
  password = request.args.get('password')
  if not password:
    raise AuthError(AuthStatus.NO_PASSWORD_SUPPLIED)
  password_hash = password_hashes.get(str(user['user_id']))
  if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
    raise AuthError(AuthStatus.INCORRECT_PASSWORD)

  combined_key = str(user_id) + app.secret_key
  token = bcrypt.hashpw(combined_key.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
  return {'user_id': user_id, 'authenticated': True, 'token': token}, HTTPStatus.OK

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
  token_raw = request.args.get('token')
  token = token_raw.encode('utf-8')
  combined_key = str(user_id) + app.secret_key
  if not bcrypt.checkpw(combined_key.encode('utf-8'), token):
    raise AuthError(AuthStatus.INVALID_APP_USER_TOKEN)
  return user_from_user_id(user_id)


