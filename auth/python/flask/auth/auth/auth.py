from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
  return render_template('index.jinja2')
