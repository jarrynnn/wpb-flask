import json

import urllib.request

connection = urllib.request.urlopen('https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json')

js = connection.read()

#print(js)
info = json.loads(js.decode("utf-8"))


country_names_list = ["afghanistan", "uk", "france"]

populations = dict()
gdp_pc = dict{}
life_expectancy = dict{}
edu_expenditure_pct_gdp = dict{}
literacy = dict{}
unemployment = dict{}
health_expenditure_pct_gdp = dict{}
pct_poverty_line = dict{}
hdi = dict()


countries_lookup = dict()
for k, v in info["countries"].items():
    countries_lookup[k] = v["data"]["name"]

for c in country_names_list:
    try :
        populations[c] = info["countries"][c]["data"]["people"]["population"]["total"]
    except:
        populations[c] = "NA"
    try:
        gdp_pc[c] = 
    except:
        gdp_pc[c] = "NA"
    try:
        gdp_pc[c] = 
    except:
        gdp_pc[c] = "NA"
    try:
        gdp_pc[c] = 
    except:
        gdp_pc[c] = "NA"
    try:
        gdp_pc[c] = 
    except:
        gdp_pc[c] = "NA"
    try:
        gdp_pc[c] = 
    except:
        gdp_pc[c] = "NA"


data = {
        "population" =  populations,
        "gdp" = gdps,




}



print(info["countries"]["world"]["data"]["people"]["population"]["total"])