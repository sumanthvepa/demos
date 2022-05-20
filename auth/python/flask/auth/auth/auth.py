import os
import secrets
from http import HTTPStatus

import requests
from flask import (
  Flask,
  abort,
  redirect,
  render_template,
  request,
  session,
  url_for)


def create_app():
  """ Create fully configured Flask auth app"""
  auth_app = Flask(__name__)
  auth_app.secret_key = os.environ.get('AUTH_APP_FLASK_SECRET_KEY')
  if auth_app.secret_key is None:
    raise RuntimeError(
      'AUTH_APP_FLASK_SECRET_KEY must be set for the auth app to run')


app = create_app()


# TODO: Get these variable from settings
AUTHWS_SERVER_URL = 'http://nines.milestone42.com:5001'
AUTHWS_USERS_URL = AUTHWS_SERVER_URL + '/api/users/'
AUTHWS_USER_URL = AUTHWS_SERVER_URL + '/api/user'


def generate_csrf_token():
  """ Generate URL save CSRF token """
  return secrets.token_urlsafe(64)


def is_valid_redirect_url(redirect_url):
  """ Return true if a redirect URL is valid. False otherwise """
  # Only redirects to specific pages are permissible.
  # This checks that the redirect is valid. If so,
  # it returns True. Otherwise, it returns False.
  valid_redirects = [url_for('home_page')]
  return redirect_url in valid_redirects


class SignInError(RuntimeError):
  """ Exception raised when a problem is encountered during signin """
  pass


def find_user_id(username_email, api_session=None):
  """ Call AuthWS to get a user_id for a given username or email """
  rq = api_session if api_session else requests
  params = {'username_email': username_email}
  r = rq.get(AUTHWS_USERS_URL, params=params)
  if r.status_code == HTTPStatus.NOT_FOUND:
    raise SignInError(
      'We could not find this username or email in our records')
  if r.status_code != HTTPStatus.OK:
    raise SignInError(
      'An internal service seems to be malfunctioning. '
      + 'Please try again shortly or contact our support staff. '
      + 'Sorry for the inconvenience')
  d = r.json()
  return d.get('user_id')


def authenticate_user_id(user_id, password, api_session=None):
  """ Call AuthWS to authenticate the given user_id with the given password """
  rq = api_session if api_session else requests
  params = {'password': password}
  r = rq.get(AUTHWS_USER_URL + '/' + str(user_id) + '/authenticate', params=params)
  if r.status_code == HTTPStatus.FORBIDDEN:
    raise SignInError(
      'The password you entered did not '
      + 'match with the one we have on file for you.')
  if r.status_code != HTTPStatus.OK:
    raise SignInError(
      'An internal service seems to be malfunctioning. '
      + 'Please try again shortly or contact our support staff. '
      + 'Sorry for the inconvenience')
  d = r.json()
  return d.get('token')


def get_user(user_id, token, api_session=None):
  """ Call AuthWS to get a user JSON dictionary given a user_id """
  if not user_id:
    return None
  rq = api_session if api_session else requests
  params = {'token': token}
  r = rq.get(AUTHWS_USER_URL + '/' + str(user_id), params=params)
  if r.status_code != HTTPStatus.OK:
    raise SignInError(
      'An internal service seems to be malfunctioning. '
      + 'Please try again shortly or contact our support staff. '
      + 'Sorry for the inconvenience')
  return r.json()


def authenticate_credentials(username_email, password):
  """ Call AuthWS to authenticate a username or email + password combination"""
  with requests.session() as api_session:
    user_id = find_user_id(username_email, api_session)
    token = authenticate_user_id(user_id, password, api_session)
    user = get_user(user_id, token, api_session)
    user['token'] = token
    return user


@app.route('/', methods=['GET'])
def home_page():
  """ Render a simple home page with either a signin or sign-out option """
  # TODO: Perhaps replace with WTForms and flask_wtforms?
  # Generate a new CSRF token. This is done
  # every time the signin form is generated.
  csrf_token = generate_csrf_token()
  session['csrf_token'] = csrf_token

  redirect_url = url_for('home_page')

  user = get_user(session.get('user_id'), session.get('user_token'))

  return render_template(
    'index.jinja2',
    user=user,
    redirect_url=redirect_url,
    csrf_token=csrf_token)


@app.route('/signin/', methods=['GET'])
def signin_page():
  """ Render a signin form """
  # Get the error object and related keys
  # These objects are set if there were errors in a previous
  # attempt at sign in, and the user is reaching this
  # URL via redirect back from a failed form processing.
  error = session.get('error', None)
  if error:
    del session['error']
  default_username_email = session.get('default_username_email', None)
  if default_username_email:
    del session['default_username_email']
  default_password = session.get('default_password', None)
  if default_password:
    del session['default_password']

  # Get the redirect URL. This will be set if
  # the Sign In is triggered by a redirect from
  # another URL (e.g. the POST /signin URL will redirect
  # the user to this page if there were errors in the
  # sign in credentials.)
  redirect_url = request.args.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  # TODO: Perhaps replace with WTForms and flask_wtforms?
  # Generate a new CSRF token. This is done
  # every time the signin form is generated.
  csrf_token = generate_csrf_token()
  session['csrf_token'] = csrf_token

  return render_template(
    'signin.jinja2',
    error=error,
    default_username_email=default_username_email,
    default_password=default_password,
    redirect_url=redirect_url,
    csrf_token=csrf_token)


@app.route('/signin/', methods=['POST'])
def process_signin():
  """ Process a signin request """
  # Reset the session user field.
  if 'user_id' in session:
    del session['user_id']
  if 'user_token' in session:
    del session['user_token']

  # Clean up the error related values in the session
  if 'error' in session:
    del session['error']
  if 'default_username_email' in session:
    del session['default_username_email']
  if 'default_password' in session:
    del session['default_password']

  # Check CSRF token and return 403 Forbidden if the
  # CSRF token does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token', None)
  session_csrf_token = session.get('csrf_token', None)
  if form_csrf_token != session_csrf_token:
    abort(HTTPStatus.FORBIDDEN)

  # Get the redirect URL from the hidden input
  # field in the form. Use that (after validation) to
  # redirect the user to the appropriate post signin
  # page.
  redirect_url = request.form.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  # Get the username and email from the form
  username_email = request.form.get('username_email', None)
  password = request.form.get('password', None)

  # Get the user by authenticating their credentials or
  # fail and take the visitor back to the signin page with errors
  try:
    user = authenticate_credentials(username_email, password)
    session['user_id'] = user['user_id']
    session['user_token'] = user['token']
    return redirect(redirect_url)
  except SignInError as ex:
    session['error'] = str(ex)
    session['default_username_email'] = username_email
    session['default_password'] = password
    return redirect(url_for('signin_page') + '?redirect_url=' + redirect_url)


@app.route('/sign-out/', methods=['POST'])
def process_sign_out():
  """ Process a sign-out request """
  # Check CSRF token and return 403 Forbidden if the CSRF token
  # does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token')
  session_csrf_token = session.get('csrf_token')
  if form_csrf_token != session_csrf_token:
    abort(HTTPStatus.FORBIDDEN)

  user = get_user(session.get('user_id'), session.get('user_token'))
  if user:
    del session['user_id']
    del session['user_token']

  redirect_url = request.form.get('redirect_url')
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  return redirect(redirect_url)
