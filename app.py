from flask import Flask, render_template, url_for, jsonify, request
from database import db_session, init_db
from models import get_countries, get_country, get_countrydatas, get_countrydatas_by_country_id, get_country_by_id, get_metrics, get_metric_by_id
import datetime
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
    #collect currentdata for all metrics
    current_year = 2018         #change this to pick up from today's date! datetime.datetime.today().year
    
    key = []
    countryname = []
    countrycolour= []
    metric= []
    region= []
    year= []
    value= []
    geo_id = []
    

    for country in country_list:
            key += ([c.id for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            value += ([c.value for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            year += ([c.year for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            countryname += ([c.country.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            countrycolour += (["#"+c.country.colour for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            metric += ([c.metric.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            region += ([c.country.region.name for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])
            geo_id += ([c.country.geo_id for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)])

    currentdata  = {   
                'key'       : key,
                'countryname'   : countryname,
                'countrycolour'   : countrycolour,
                'geo_id'    : geo_id,
                'metric'     :metric,
                'region'    : region,
                'year'      : year,
                'value'    : value,
            }

    #if there is also trends data for that metric, bring back all years as list (per country) of dicts (per year-value datapoints} for each country
    if sel_metric.trends_switch: 
        years_list = list(range(current_year-19, current_year+1))
        trends_data = []
        for year in years_list:
            for country in country_list:
            
                trends_data += [
                    {'key'       : c.id,
                'country'   : c.country.name,
                'geo_id'    : c.country.geo_id,
                'metric'     :c.metric.name,
                'region'    : c.country.region.name,
                'year'      : year,
                'value'    : c.value} for c in get_countrydatas_by_country_id(country, sel_metric.id, year)]
    else:
        trends_data= []
        years_list = list(current_year)

    mapdata = []
    for country in country_list:
        mapdata += [          
             {'id'    : c.country.geo_id,
             'value'    : c.value} for c in get_countrydatas_by_country_id(country, sel_metric.id, current_year)]

    return jsonify(data=currentdata, mapdata = mapdata, years_list = years_list, trends_data = trends_data)


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