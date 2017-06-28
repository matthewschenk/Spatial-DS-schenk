import json
import os,sys
import pprint as pp
import collections

f = open('./json_files/state_borders.json','r')
data = f.read()
data = json.loads(data)

all_states = []
i = -1
for s in data:
    gj = collections.OrderedDict()
    gj['type'] = 'Feature'
    gj['properties'] = s
    stateline = s['borders']
    del gj['properties']['borders']
    gj['geometry'] = {}
    gj['geometry']['type'] = 'Polygon'
    gj['geometry']['coordinates'] = stateline
    i = i + 1
    if i < 1000:
        all_states.append(gj)

#pp.print(all_states)

out = open('./1000states.geojson','w')
out.write(json.dumps(all_states, sort_keys=False, indent=4, separators=(',',': ')))
out.close()


