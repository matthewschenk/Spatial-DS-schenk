import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/world_cities_large.json','r')
data = f.read()
data = json.loads(data)

all_cities = []
i = -1
for k,v in data.items():
    #k = year
    #v = object of properties
    for c in v:
        #print(q)
        gj = collections.OrderedDict()
        gj['type'] = 'Feature'
        gj['properties'] = c
        lat = c['lat']
        if lat != "":
            lat = float(lat)
        lon = c['lon']
        if lon != "":
            lon = float(lon)
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj['geometry'] = {}
        gj['geometry']['type'] = 'Point'
        gj['geometry']['coordinates']=[lon,lat]
        i = i + 1
        if i < 1000:
            all_cities.append(gj)

#pp.print(all_airports)

out = open('./1000cities.geojson','w')
out.write(json.dumps(all_cities, sort_keys=False, indent=4, separators=(',',': ')))
out.close()