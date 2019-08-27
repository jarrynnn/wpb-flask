import json
import urllib.request
import pandas as pd

connection = urllib.request.urlopen('https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json')

js = connection.read()

info = json.loads(js.decode("utf-8"))


country_names_list = ["afghanistan", "uk", "france"]

populations = dict()
gdp_pc = dict()
gdp_rank = dict()
life_expectancy = dict()
edu_expenditure_pct_gdp = dict()
literacy = dict()
unemployment = dict()
health_expenditure_pct_gdp = dict()
pct_poverty_line = dict()


countries_lookup = dict()
for k, v in info["countries"].items():
    countries_lookup[k] = v["data"]["name"]

for c, v in countries_lookup.items() :
    try :
        populations[v] = info["countries"][c]["data"]["people"]["population"]["total"]
    except:
        populations[v] = "NA"
    try:
        #annual values given as a list of dicts with the latest in the first index posisiton 
        gdp_pc[v] = info["countries"][c]["data"]["economy"]["gdp"]["per_capita_purchasing_power_parity"]["annual_values"][0]["value"]
        gdp_rank[v] = info["countries"][c]["data"]["economy"]["gdp"]["per_capita_purchasing_power_parity"]["global_rank"] 
    except:
        gdp_pc[v] = "NA"
        gdp_rank[v] = "NA"
    try:
        pct_poverty_line[v] = info["countries"][c]["data"]["economy"]["population_below_poverty_line"]["value"]
    except:
        pct_poverty_line[v] = "NA"
    try:
        #annual values given as a list of dicts with the latest in the first index posisiton 
        unemployment[v] = info["countries"][c]["data"]["economy"]["unemployment_rate"]["annual_values"][0]["value"]
    except:
        unemployment[v] = "NA"
    try:
        edu_expenditure_pct_gdp[v] = info["countries"][c]["data"]["people"]["education_expenditures"]["percent_of_gdp"]
    except:
        edu_expenditure_pct_gdp[v] = "NA"
    try:
        health_expenditure_pct_gdp[v] = info["countries"][c]["data"]["people"]["health_expenditures"]["percent_of_gdp"]
    except:
        health_expenditure_pct_gdp[v] = "NA"
    try:
        life_expectancy[v] = info["countries"][c]["data"]["people"]["life_expectancy_at_birth"]["total_population"]["value"]
    except:
        life_expectancy[v] = "NA"
    try:
        literacy[v] = info["countries"][c]["data"]["people"]["literacy"]["total_population"]["value"]
    except:
        literacy[v] = "NA"


data = {
        "population" :  populations,
        "gdp" : gdp_pc,
        "gdp_rank" : gdp_rank,
        "life_expectancy" : life_expectancy,
        "edu_expenditure_pct_gdp" : edu_expenditure_pct_gdp,
        "literacy" : literacy,
        "unemployment" : unemployment,
        "health_expenditure_pct_gdp" : health_expenditure_pct_gdp,
        "pct_poverty_line" : pct_poverty_line
        }


df = pd.DataFrame(data)
df.to_csv("cia_data.csv")


print(df)