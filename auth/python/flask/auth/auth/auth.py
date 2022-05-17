import os
import secrets

import bcrypt
from flask import (
  Flask,
  abort,
  redirect,
  render_template, 
  request,
  session,
  url_for)

app = Flask(__name__)

app.secret_key = os.environ.get('AUTH_APP_FLASK_SECRET_KEY')
if app.secret_key is None:
  raise RuntimeError(
    'AUTH_APP_FLASK_SECRET_KEY must be set for the auth app to run')

def generate_csrf_token():
  return secrets.token_urlsafe(64)

def is_valid_redirect_url(redirect_url):
  # Only redirects to specific pages are permissible.
  # This checks that the redirect is valid. If so,
  # it returns True. Otherwise, it returns False.
  VALID_REDIRECTS = [url_for('home_page')]
  return redirect_url in VALID_REDIRECTS

class SignInError(RuntimeError):
  pass

# TODO: Move these dictionaries to authws and fetch them from the database
users = {
  '1': {
    'user_id': 1,
    'username': 'luser',
    'email': 'luser@example.com',
    'display_name': 'Lawrence Un Ser',
    'password_hash':
      bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt(12))
  }
}

by_username = dict(zip([user['username'] for user in users.values()], users.values()))
by_email = dict(zip([user['email'] for user in users.values()], users.values()))


def find_user_by_username(username):
  return by_username.get(username, None)


def find_user_by_email(email):
   return by_email.get(email, None)


def find_user_by_username_or_email(username_email):
  user = find_user_by_username(username_email)
  if not user:
    user = find_user_by_email(username_email)
  return user


def authenticate_credentials(username_email, password):
  user = find_user_by_username_or_email(username_email)
  if not user:
    raise SignInError(
      'We could not find this username or email in our records')

  password = password.encode('utf-8')
  if not bcrypt.checkpw(password, user.get('password_hash')):
    raise SignInError(
      'The password you entered did not '
      + 'match with the one we have on file for you.')

  return user


def user_from_user_id(user_id):
  return users.get(str(user_id), None)


@app.route('/', methods=['GET'])
def home_page():
  # TODO: Perhaps replace with WTForms and flask_wtforms?

  # Generate a new CSRF token. This is done
  # every time the signin form is generated.
  csrf_token = generate_csrf_token()
  session['csrf_token'] = csrf_token

  redirect_url = url_for('home_page')

  user = user_from_user_id(session.get('user_id', None))

  return render_template(
      'index.jinja2',
      user=user, 
      redirect_url=redirect_url,
      csrf_token=csrf_token)


@app.route('/signin/', methods=['GET'])
def signin_page():
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

  # Get the redirect URL (This will be set if 
  # if the Sign In is triggered by a redirect from
  # another URL (e.g. the POST /signin URL will redirect
  # the user to this page if there were errors in the
  # sign in credentials.
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
  # Reset the session user field.
  if 'user_id' in session:
    del session['user_id']

  # Clean up the error related values in the session
  if 'error' in session:
    del session['error']
  if 'default_username_email' in session:
    del session['default_username_email']
  if 'default_password' in session:
    del session['default_password']

  # Check CSRF token and return 401 if the CSRF token
  # does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token', None)
  session_csrf_token = session.get('csrf_token', None)
  if form_csrf_token != session_csrf_token:
    abort(401)

  # Get the redirect URL from the from the hidden input
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
    return redirect(redirect_url)
  except SignInError as ex:
    session['error'] = str(ex)
    session['default_username_email'] = username_email
    session['default_password'] = password
    return redirect(url_for('signin_page') + '?redirect_url='+redirect_url)
  

@app.route('/signout/', methods=['POST'])
def process_signout():
  # Check CSRF token and return 401 if the CSRF token
  # does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token', None)
  session_csrf_token = session.get('csrf_token', None)
  if form_csrf_token != session_csrf_token:
    abort(401)

  user = user_from_user_id(session.get('user_id', None))
  if user:
    del session['user_id']

  redirect_url = request.form.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  return redirect(redirect_url)
