import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/earthquakes-1960-2017.json','r')
data = f.read()
data = json.loads(data)

all_earthquakes = []
#print(data)
i = -1
for k,v in data.items():
    #k = year
    #v = object of properties
    for q in v:
        #print(q)
        gj = collections.OrderedDict()
        gj['type'] = 'Feature'
        gj['properties'] = q
        geo = {}
        geo = q['geometry']
        del gj['properties']['geometry']
        gj['properties']['year'] = k
        gj['geometry'] = {}
        gj['geometry'] = geo
        i = i + 1
        if i < 1000:
            all_earthquakes.append(gj)

#pp.print(all_earthquakes)

out = open('./1000earthquakes.geojson','w')
out.write(json.dumps(all_earthquakes, sort_keys=False, indent=4, separators=(',',': ')))
out.close()
