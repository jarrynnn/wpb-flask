from flask import Flask
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"