from flask import Flask, render_template, url_for, jsonify
from database import db_session, init_db
from models import get_countries, get_country, get_countrydatas, get_countrydatas_by_country_id, get_country_by_id

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
    
    return jsonify(status="Database Initialised")

@app.route("/")
def home():
    return render_template(
        'home.html',
        page = 'Home',
        **default_context()
    )

@app.route("/data/<countryref_id>")
def data(countryref_id=None):
    country = get_country_by_id(countryref_id)
    country_datas = get_countrydatas_by_country_id(countryref_id)
    if country is None:
        data = [
            {   'year' : c.year,
                'value' : c.value,
            } for c in get_countrydatas_by_country_id(country.id)
        ]

    else:  
        key = [c.id for c in get_countrydatas_by_country_id(country.id)] 
        value = [c.value for c in get_countrydatas_by_country_id(country.id)] 
        year = [c.year for c in get_countrydatas_by_country_id(country.id)] 
        data  = {   
                'key'       : key,
                #'country'   : c.country.name,
                #'metric'     :c.metric.name,
                #'region'    : c.country.region.name,
                'year'      : year,
                'value'    : value,
            } 
        

    return jsonify(data=data)


@app.route("/countries")
@app.route("/countries/<country>")
def countries(country_name=None):
    return render_template(
        'countries.html',
        country_list = [
            {
                'key'       : c.id,
                'label'     : c.name,
                'region_id' : c.region_id,
                'region'      : c.region,
                'colour'    : "#" + c.colour,
                'country_datas' : c.country_datas,
                'similar_countries' : c.similar_countries,
                'url'       : url_for('countries', country_name=c.name)
            } for c in get_countries()
        ],
        country = get_country(country_name), 
        country_datas_list = [            
            {
            'key'       : c.id,
            'country'   : c.country,
            'metric'     :c.metric,
            'region'    : c.country.region,
            'year'      : c.year,
            'value'    : c.value,
        } for c in get_countrydatas_by_country_id(country.id)
        ] if country_name is not None else get_countrydatas(),

        page = 'All Countries' if country_name is None else country_name,
        **default_context()
    )