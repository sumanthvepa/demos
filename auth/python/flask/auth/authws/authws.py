from flask import Flask


app = Flask(__name__)


@app.route('/api/users/', methods=['GET'])
def find_user():
  return {"user_id": 1}
