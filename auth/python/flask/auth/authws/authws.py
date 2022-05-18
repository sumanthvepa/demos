from http import HTTPStatus

import bcrypt
from flask import Flask, Response, request


app = Flask(__name__)



@app.route('/api/users/', methods=['GET'])
def find_user():
  return {"user_id": 1}
