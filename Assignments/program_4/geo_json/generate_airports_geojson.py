import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/airports.json','r')
data = f.read()
data = json.loads(data)

all_airports = []
i = -1
for k,v in data.items():
    gj = collections.OrderedDict()
    gj['type'] = 'Feature'
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Point'
    gj['geometry']['coordinates']=[lon,lat]
    i = i + 1
    if i < 1000:
        all_airports.append(gj)

#pp.print(all_airports)

out = open('./1000airports.geojson','w')
out.write(json.dumps(all_airports, sort_keys=False, indent=4, separators=(',',': ')))
out.close()