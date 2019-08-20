from flask import Flask, render_template, url_for, jsonify, request
from database import db_session, init_db
from models import get_countries, get_country, get_countrydatas, get_countrydatas_by_country_id, get_country_by_id, get_metrics, get_metric_by_id

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


@app.route("/data/<countryref_ids>")
def data(countryref_ids=None):

    country_list = countryref_ids.split(',')
    key = []
    countryname = []
    countrycolour= []
    metric= []
    region= []
    year= []
    value= []
    for country in country_list:
        key += ([c.id for c in get_countrydatas_by_country_id(country)])
        value += ([c.value for c in get_countrydatas_by_country_id(country)])
        year += ([c.year for c in get_countrydatas_by_country_id(country)])
        countryname += ([c.country.name for c in get_countrydatas_by_country_id(country)])
        countrycolour += (["#"+c.country.colour for c in get_countrydatas_by_country_id(country)])
        metric += ([c.metric.name for c in get_countrydatas_by_country_id(country)])
        region += ([c.country.region.name for c in get_countrydatas_by_country_id(country)])

    data  = {   
                'key'       : key,
                'countryname'   : countryname,
                'countrycolour'   : countrycolour,
                'metric'     :metric,
                'region'    : region,
                'year'      : year,
                'value'    : value,
            }  

    return jsonify(data = data)

@app.route("/data/<countryref_ids>/<metric_id>")
def metricdata(countryref_ids=None, metric_id=1):
    country_list = countryref_ids.split(',')
    sel_metric = get_metric_by_id(metric_id)
    if not sel_metric.trends_switch: #if there are no trends data, just look for current year, otherwise bring back all years -may need ot think abou thow this brought back
        current_year = 2018         #change this to pick up from today's date!
    else: 
        current_year = None
    

    key = []
    countryname = []
    countrycolour= []
    metric= []
    region= []
    year= []
    value= []
    
    for country in country_list:
        key += ([c.id for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        value += ([c.value for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        year += ([c.year for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        countryname += ([c.country.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        countrycolour += (["#"+c.country.colour for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        metric += ([c.metric.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
        region += ([c.country.region.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])

    data  = {   
                'key'       : key,
                'countryname'   : countryname,
                'countrycolour'   : countrycolour,
                'metric'     :metric,
                'region'    : region,
                'year'      : year,
                'value'    : value,
            }       

    return jsonify(data=data)


@app.route("/countries")
@app.route("/countries/<country_name>")
def countries(country_name=None):
    return render_template(
        'countries.html',
        metric_list = [
            {
                'key'       : m.id,
                'label'     : m.name,
                'trends_switch' : m.trends_switch,
            } for m in get_metrics()
        ],
        country_list = [
            {
                'key'       : c.id,
                'label'     : c.name,
                'geo_id'    : c.geo_id,
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
            'geo_id'    : c.country.geo_id,
            'metric'     :c.metric,
            'region'    : c.country.region,
            'year'      : c.year,
            'value'    : c.value,
        } for c in get_countrydatas_by_country_id(country.id)
        ] if country_name is not None else get_countrydatas(),

        page = 'All Countries' if country_name is None else country_name,
        **default_context()
    )