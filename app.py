from flask import Flask, render_template
from database import db_session, init_db
from models import get_countries

import json

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/init_db")
def init_db():
    status = "Database Initialised"
    try:
        init_db(create_test_data=True)
    finally:
        return json.dumps({"status": status})

@app.route("/")
def home():
    return ",".join([str(i) for i in get_countries()])