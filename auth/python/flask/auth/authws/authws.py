#####################################################################
# This file is part of demos.
# Demos is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Demos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <https://www.gnu.org/licenses/>.
#####################################################################

import os
from enum import Enum
from http import HTTPStatus

import bcrypt
from werkzeug.exceptions import HTTPException
from flask import Flask, request


def create_app():
  """ Create a properly configured auth web service app"""
  authws_app = Flask(__name__)
  authws_app.secret_key = os.environ.get('AUTHWS_FLASK_SECRET_KEY')
  if authws_app.secret_key is None:
    raise RuntimeError(
      'AUTHWS_FLASK_SECRET_KEY must be set for the auth app to run')
  return authws_app


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


def find_user_by_username(username):
  # TODO: Replace this with real code
  return by_username.get(username, None)


def find_user_by_email(email):
  # TODO: Replace this with real code.
  return by_email.get(email, None)


def find_user_by_username_or_email(username_email):
  # TODO: Replace this with real code.
  from_username = find_user_by_username(username_email)
  from_email = find_user_by_email(username_email)
  user = from_username or from_email
  if not user:
    raise AuthError(AuthStatus.NO_SUCH_USER)
  return user


def user_from_user_id(user_id):
  # TODO: Replace this with real code.
  user = users.get(str(user_id), None)
  if not user:
    raise AuthError(AuthStatus.NO_SUCH_USER)
  return user


@app.route('/api/users/', methods=['GET'])
def find_user():
  """ Return user id given a username or email """
  username_email = request.args.get('username_email')
  if not username_email:
    raise AuthError(AuthStatus.NO_USERNAME_EMAIL_SUPPLIED)
  return {'user_id': find_user_by_username_or_email(username_email)['user_id']}


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
  password_hash = password_hashes.get(str(user['user_id']))
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
