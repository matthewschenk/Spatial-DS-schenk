import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/world_volcanos.json','r')
data = f.read()
data = json.loads(data)

all_volcanos = []
i = -1
for v in data:
    gj = collections.OrderedDict()
    gj['type'] = 'Feature'
    gj['properties'] = v
    lat = v['Lat']
    if lat != "":
        lat = float(lat)
    lon = v['Lon']
    if lon != "":
        lon = float(lon)
    del gj['properties']['Lat']
    del gj['properties']['Lon']
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Point'
    gj['geometry']['coordinates']=[
      lon,
      lat
    ]
    i = i + 1
    if i < 1000:
        all_volcanos.append(gj)
#pp.print(all_volcanos)

out = open('./1000volcanos.geojson','w')
out.write(json.dumps(all_volcanos, sort_keys=False, indent=4, separators=(',',': ')))
out.close()