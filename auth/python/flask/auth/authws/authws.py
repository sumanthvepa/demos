#####################################################################
# This file is part of demos project.
# (https://github.com/sumanthvepa/demos)
#
# Copyright (c) 2022 Sumanth Vepa.

# Demos is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Demos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <https://www.gnu.org/licenses/>.
#####################################################################

import os
from enum import Enum
from http import HTTPStatus
from urllib.parse import quote

import bcrypt
from werkzeug.exceptions import HTTPException
from flask import Flask, request
from sqlalchemy import create_engine, text


def get_required_environment_variable(variable_name, error_message):
  variable = os.environ.get(variable_name)
  if not variable:
    raise RuntimeError(error_message)
  return variable


def create_db():
  db_host = get_required_environment_variable(
    'AUTHWS_DB_HOST',
    'AUTHWS_DB_HOST environment variable must be set for the '
    + 'authws webservice to run')
  db_host = quote(db_host.strip())

  db_name = get_required_environment_variable(
    'AUTHWS_DB_NAME',
    'AUTHWS_DB_NAME environment variable must be set for the '
    + 'authws webservice to run')
  db_name = quote(db_name.strip())

  db_user = get_required_environment_variable(
    'AUTHWS_DB_USER',
    'AUTHWS_DB_USER environment variable must be set for the '
    + 'authws webservice to run')
  db_user = quote(db_user.strip())

  db_password = get_required_environment_variable(
    'AUTHWS_DB_PASSWORD',
    'AUTHWS_DB_PASSWORD environment variable must be set for the '
    + 'authws webservice to run')
  db_password = quote(db_password.strip())

  connect_url = f'mariadb+pymysql://' \
      + f'{db_user}:{db_password}@{db_host}/{db_name}' \
      + f'?charset=utf8mb4'
  return create_engine(connect_url, echo=False, future=True, pool_recycle=3600)


def create_app():
  """ Create a properly configured auth web service app"""
  authws_app = Flask(__name__)
  authws_app.secret_key = get_required_environment_variable(
    'AUTHWS_FLASK_SECRET_KEY',
    'AUTHWS_FLASK_SECRET_KEY must be set for the auth app to run')
  return authws_app


db = create_db()
app = create_app()


class AuthStatus(Enum):
  """ A Smart Enum that that describes all the errors that can possibly
      occur in the operation of the auth web service """

  def __new__(cls, *args, **kwargs):
    """
      This method assigns every member of this enum a distinct
      ordinal count that enables each enum member to have distinct
      value. (This is different from the error_code which need not
      be sequentially assigned)
    """
    value = len(cls.__members__) + 1
    obj = object.__new__(cls)
    obj._value = value
    return obj

  def __init__(self, http_status, description):
    """
      Initializes an enum instance with an error_code, http status and error
      description
    """
    super().__init__()
    self.error_code = self._value - 1
    self.http_status = http_status
    self.description = description

  def to_tuple(self, additional_description=None):
    description = self.description
    if additional_description:
      description += ': ' + additional_description
    return tuple(
      [{'error_code': self.error_code, 'error_message': description},
       self.http_status])

  SUCCESS = HTTPStatus.OK, 'Ok'
  NO_USERNAME_EMAIL_SUPPLIED \
      = HTTPStatus.BAD_REQUEST, 'Query parameter username_email not supplied'
  NO_SUCH_USER \
      = HTTPStatus.NOT_FOUND, 'No such user'
  NO_PASSWORD_SUPPLIED \
      = HTTPStatus.BAD_REQUEST, 'Query parameter password not supplied'
  INCORRECT_PASSWORD \
      = HTTPStatus.FORBIDDEN, 'Incorrect password'
  NO_USER_TOKEN_SUPPLIED \
      = HTTPStatus.BAD_REQUEST, 'Query parameter token was not supplied'
  INVALID_APP_USER_TOKEN \
      = HTTPStatus.BAD_REQUEST, 'Invalid application user token'
  CORRUPTED_DATABASE_TOO_MANY_USER_IDS \
      = HTTPStatus.INTERNAL_SERVER_ERROR,\
        'Corrupted database too many internal user_ids found for the given username or email'
  CLIENT_ERROR \
      = HTTPStatus.BAD_REQUEST, 'Client error'
  INTERNAL_ERROR \
      = HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal error'
  OTHER_ERROR \
      = HTTPStatus.INTERNAL_SERVER_ERROR, 'Other error'


class AuthError(RuntimeError):
  """ The exception raised when the auth web service encounters a problem"""

  def __init__(self, status):
    super().__init__(status.description)
    self.status = status

  def to_tuple(self):
    return self.status.to_tuple()


@app.errorhandler(AuthError)
def handle_authentication_errors(ex):
  """ Convert AuthError into a JSON error response """
  return ex.to_tuple()


@app.errorhandler(HTTPException)
def handle_http_exceptions(ex):
  """ Convert HTTPException into a JSON error response"""
  auth_status = AuthStatus.OTHER_ERROR
  if 400 <= ex.code < 500:
    auth_status = AuthStatus.CLIENT_ERROR
  if ex.code >= 500:
    auth_status = AuthStatus.INTERNAL_ERROR
  return auth_status.to_tuple(str(ex))


@app.errorhandler(Exception)
def handle_errors(ex):
  """
    Convert Exception into a JSON error response

    This is a catchall error handler.
  """
  return AuthStatus.INTERNAL_ERROR.to_tuple(str(ex))


# TODO: Get all this data from a DB. This is dummy code.
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


def db_result_to_tuple(result):
  return [tuple(row) for row in result.all()]


def find_user_id_by_username_or_email(username_email):
  with db.connect() as connection:
    sql = "select user_id from username where username = :username_email " \
          + "union " \
          + "select user_id from email where email = :username_email "
    bind_variables = {'username_email': username_email}
    result = db_result_to_tuple(connection.execute(text(sql), bind_variables))
    if len(result) < 1:
      raise AuthError(AuthStatus.NO_SUCH_USER)
    if len(result) > 1:
      raise AuthError(AuthStatus.CORRUPTED_DATABASE_TOO_MANY_USER_IDS)
    return result[0][0]


def password_hash_from_user_id(user_id):
  with db.connect() as connection:
    sql = "select password_hash from password where user_id = :user_id"
    bind_variables = {'user_id': int(user_id)}
    result = db_result_to_tuple(connection.execute(text(sql), bind_variables))
    if len(result) < 1:
      raise AuthError(AuthStatus.NO_SUCH_USER)
    if len(result) > 1:
      raise AuthError(AuthStatus.CORRUPTED_DATABASE_TOO_MANY_USER_IDS)
    return result[0][0]


def user_from_user_id(user_id):
  with db.connect() as connection:
    sql = "select user.user_id, username.username, email.email, user.display_name" \
          + " from user left join username on user.user_id = username.user_id " \
          + "left join email on email.user_id = user.user_id where user.user_id = :user_id"
    bind_var = {'user_id': int(user_id)}
    result = db_result_to_tuple(connection.execute(text(sql), bind_var))
    if len(result) < 1:
      raise AuthError(AuthStatus.NO_SUCH_USER)
    if len(result) > 1:
      raise AuthError(AuthStatus.CORRUPTED_DATABASE_TOO_MANY_USER_IDS)
    return dict(zip(['user_id', 'username', 'email', 'display_name'], list(result[0])))


@app.route('/api/users/', methods=['GET'])
def find_user():
  """ Return user id given a username or email """
  username_email = request.args.get('username_email')
  if not username_email:
    raise AuthError(AuthStatus.NO_USERNAME_EMAIL_SUPPLIED)
  return {'user_id': find_user_id_by_username_or_email(username_email)}


@app.route('/api/user/<int:user_id>/authenticate', methods=['GET'])
def authenticate_user(user_id):
  """
    Authenticate a user given a user id and password.

    Returns a JSON object with a token that can be used for further
    queries.

  """
  user = user_from_user_id(user_id)
  password = request.args.get('password')
  if not password:
    raise AuthError(AuthStatus.NO_PASSWORD_SUPPLIED)

  password_hash = password_hash_from_user_id(user_id).encode('utf-8')

  if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
    raise AuthError(AuthStatus.INCORRECT_PASSWORD)

  combined_key = str(user_id) + app.secret_key
  token = bcrypt.hashpw(combined_key.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
  return {'user_id': user_id, 'authenticated': True, 'token': token}, HTTPStatus.OK


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
  """
    Return a JSON user object for a given user id.

    The caller must supply a user authentication token in the
    query parameters.
  """
  token_raw = request.args.get('token')
  if not token_raw:
    raise AuthError(AuthStatus.NO_USER_TOKEN_SUPPLIED)
  token = token_raw.encode('utf-8')
  combined_key = str(user_id) + app.secret_key
  if not bcrypt.checkpw(combined_key.encode('utf-8'), token):
    raise AuthError(AuthStatus.INVALID_APP_USER_TOKEN)
  return user_from_user_id(user_id)
