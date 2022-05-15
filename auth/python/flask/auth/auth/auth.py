import os
import secrets
from flask import (
  Flask,
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
  # Otherwise 
  # This checks that the redirect is valid. If so
  # it returns True. Otherwise, it returns False.
  VALID_REDIRECTS = [url_for('home_page')]
  return redirect_url in VALID_REDIRECTS


def authenticate_credentials(username_email, password):
  # TODO: Implement this.
  return {
    'username': 'sumanthvepa',
    'display_name': 'Sumanth Vepa',
    'email': 'svepa@milestone42.com' }

@app.route('/', methods=['GET'])
def home_page():
  # TODO: Perhaps replace with WTForms and flask_wtforms?
  # Generate a new CSRF token. This is done
  # every time the signin form is generated.
  csrf_token = generate_csrf_token()
  session['csrf_token'] = csrf_token

  redirect_url = url_for('home_page')

  user = session.get('user', None)
  return render_template(
      'index.jinja2',
      user=user, 
      redirect_url=redirect_url,
      csrf_token=csrf_token)


@app.route('/signin/', methods=['GET'])
def signin_page():
  # Get any error object in the session
  # This object is set if there were errors in a previous
  # attempt at sign in, and the user is reaching this
  # URL via redirect back from a failed form processing.
  error = session.get('error', None)

  # Get the redirect URL (This will be set if 
  # if the Sign In is triggered by a redirect from
  # another URL (e.g. the POST /signin URL will redirect
  # the user to this page if there were errors in the
  # sign in credentials.
  redirect_url = request.args.get('redirect_url', None)
  #redirect_url = session.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')
    #session['redirect_url'] = redirect_url

  # TODO: Perhaps replace with WTForms and flask_wtforms?
  # Generate a new CSRF token. This is done
  # every time the signin form is generated.
  csrf_token = generate_csrf_token()
  session['csrf_token'] = csrf_token

  return render_template(
    'signin.jinja2',
    error=error,
    redirect_url=redirect_url,
    csrf_token=csrf_token)

@app.route('/signin/', methods=['POST'])
def process_signin():
  # TODO: Check CSRF token and return 401 if the CSRF token
  # does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token', None)
  session_csrf_token = session.get('csrf_token', None)
  if form_csrf_token != session_csrf_token:
    abort(401)

  username_email = request.form.get('username_email', None)
  password = request.form.get('password', None)

  redirect_url = request.form.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  # Reset the session error field.
  if 'error' in session:
    del session['error']

  # Reset the session user field.
  if 'user' in session:
    del session['user']

  user = authenticate_credentials(username_email, password)
  session['user'] = user

  return redirect(redirect_url)
  

@app.route('/signout/', methods=['POST'])
def process_signout():
  # TODO: Check CSRF token and return 401 if the CSRF token
  # does not match the one stored in the session.
  form_csrf_token = request.form.get('csrf_token', None)
  session_csrf_token = session.get('csrf_token', None)
  if form_csrf_token != session_csrf_token:
    abort(401)

  user = session.get('user', None)
  if user:
    del session['user']

  redirect_url = request.form.get('redirect_url', None)
  if not is_valid_redirect_url(redirect_url):
    redirect_url = url_for('home_page')

  return redirect(redirect_url)
  
