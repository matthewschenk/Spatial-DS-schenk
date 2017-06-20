import requests
import json
import sys
import glob

"""
This class helps read the earthquake data.
Usage:
    fh = FileHelper()

    data = fh.get_data([2017]) #pass year in as list, get data for that year
    data = fh.get_data([2015,2016,2017]) #pass years in as list, get data for those years
"""


def condense_file(data):
    condensed_data = []

    for quake in data['features']:
        keep = {}
        keep['geometry'] = quake['geometry']
        keep['mag'] = quake["properties"]["mag"]
        keep['magType'] = quake["properties"]["magType"]
        keep['time'] = quake["properties"]["time"]
        keep['place'] = quake["properties"]["place"]
        keep['types'] = quake["properties"]["types"]
        keep['rms'] = quake["properties"]["rms"]
        keep['sig'] = quake["properties"]["sig"]
        condensed_data.append(keep)

    return condensed_data
    

##########################################################################################

def get_earth_quake_data(year,month=[1,12],minmag=None,maxmag=None,query=True):
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude='+str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude='+str(minmag)
    else:
        minmag = '&minmagnitude='+str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/'+type+'?format=geojson&starttime='+str(year)+'-'+str(start_month)+'-01&endtime='+str(year)+'-'+str(end_month)+'-01'+minmag+maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r

path = '/Volumes/1TBHDD/code/repos/0courses/4553-Spatial-DS/Resources/EarthquakeData'
years = [x for x in range(1960,2017)]
months = [x for x in range(0,12)]

#years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
#https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=1960-01-01&endtime=2017-01-01&minmag=7
#count = 801

for y in years:
    print("Year:%s" % (y))
    r = get_earth_quake_data(y,[1,12],7,None,True)
    f = open('./quake_data/quake-'+str(y)+'.json','w')
    f.write(json.dumps(r, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()
    rc = condense_file(r)
    f = open('./quake_data/quake-'+str(y)+'-condensed.json','w')
    f.write(json.dumps(rc, sort_keys=True,indent=4, separators=(',', ': ')))
    f.close()


