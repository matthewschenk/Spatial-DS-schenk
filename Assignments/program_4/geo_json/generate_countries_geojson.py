import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/countries.geo.json','r')
data = f.read()
data = json.loads(data)

i = -1
all_countries = []
data = data["features"]
for c in data:
    #print(c)
    gj = collections.OrderedDict()
    gj['type'] = 'Feature'
    gj['properties'] = c
    del gj['properties']['type']
    gj['properties']['name'] = gj['properties']['properties']['name']
    del gj['properties']['properties']['name']
    del gj['properties']['properties']
    gj['geometry'] = gj['properties']['geometry']
    del gj['properties']['geometry']
    i = i + 1
    if i < 1000:
        all_countries.append(gj)


#pp.print(all_cities)


out = open('./1000countries.geojson','w')
out.write(json.dumps(all_countries, sort_keys=False, indent=4, separators=(',',': ')))
out.close()