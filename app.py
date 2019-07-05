from flask import Flask, render_template, url_for
from database import db_session, init_db
from models import get_countries, get_country

import json

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def default_context():
    return {
        'home_url'          : url_for('home'),
        'countries_url'     : url_for('countries')
    }


@app.route("/initialise")
def initialise():
    init_db(create_test_data=True)
    
    return json.dumps({"status": "Database Initialised"})

@app.route("/")
def home():
    return render_template(
        'home.html',
        page = 'Home',
        **default_context()
    )

@app.route("/countries")
@app.route("/countries/<country_name>")
def countries(country_name=None):
    return render_template(
        'countries.html',
        country_list = [
            {
                'label'     : c.name,
                'stat'      : c.stat,
                'colour'    : "#" + c.colour,
                'url'       : url_for('countries', country_name=c.name)
            } for c in get_countries()
        ],
        country = get_country(country_name),
        page = 'All Countries' if country_name is None else country_name,
        **default_context()
    )