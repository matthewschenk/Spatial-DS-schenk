"""
Program:
--------

    Program 5 - Query 2

Description:
------------
    

Name: Matthew Schenk
Date: 5 July 2017
"""

import pygame
import sys,os
import json
import math
from pymongo import MongoClient
import pprint as pp

class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.world_data.airports
        self.db_cities = self.client.world_data.cities
        self.db_countries = self.client.world_data.countries
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_meteorites = self.client.world_data.meteorties
        self.db_states = self.client.world_data.states
        self.db_terrorism = self.client.world_data.terrorism
        self.db_volcanos = self.client.world_data.volcanos
    
    def get_nearest_neighbor(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_ap.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        min = 999999
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            d = self._haversine(lon,lat,lon2,lat2)
            if d < min:
                min = d
                print(d)
                print(ap['properties']['ap_name'])
                closest_ap = ap

        return closest_ap

    
    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331) must be in longitutde and latitude
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
        """
        x,y = point

        res = self.client['world_data'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )
        
        return self._make_result_list(res)

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list


def mercX(lon,zoom = 1):
    """
    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    """
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)

def mercToLL(point):
    lng,lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)
    
def toLL(point):
    x,y = point
    return mercToLL((x/4,y/4))

def adjust_point(self,p):

    lon,lat = p
    x = (mercX(lon) / 1024 * self.screen_width)
    y = (mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
    return (x,y)




if __name__=='__main__':

    pygame.init()
    bg = pygame.image.load("./worldmap.png")

    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query 2')
    screen.fill(background_colour)
    
    #example sys.arg pass in parameters
    #bob = sys.arg[0]
    #Passed in Arguments via commandline

    #Volcanos, Earthquakes, Meteorites
    if len(sys.argv) != 2:
        feature = 'volcanos'
        feature = sys.argv[1]
        if feature == 'volcanos':
            color = (255,0,0)
        elif feature == 'earthquakes':
            color = (0,0,255)
        elif feature == 'meteorites':
            color = (0,255,0)

        #All of these are in the properties: dictionary
        #Volcanos: Altitude, Country, Name, Type
        #Earthquakes: Magnitude
        #Meteorites: nametype, recclass, name, year, mass, fall, id
        field = 'year'
        field = sys.argv[2]
        #value in which to compare with
        field_value = 1900
        field_value = int(sys.argv[3])
        #Results in a greater than or less than field value ('min' or 'max')
        minimum_maximum = 'min'
        minimum_maximum = sys.argv[4]
        #Number of min or max results, 0 is all
        min_max_results = 10
        min_max_results = int(sys.argv[5])
        #Search radius from point/mouse click
        query_radius = 500
        query_radius = int(sys.argv[6])

        #Opitional
        #mx = sys.argv[7]
        #my = sys.argv[8]
    
    else:
        query_radius = int(sys.argv[1])

    mh = mongoHelper()
    flist = []  
    plot = []


    running = True
    while running:
        screen.blit(bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(sys.argv) != 2:
                    mx, my = pygame.mouse.get_pos()
                    print (mx, my)
                    my = abs(512 - my)
                    point = toLL((mx,my))
                    print(point) #Getting wrong lon,lat coords
                    feature_list = mh.get_features_near_me(feature,point,query_radius)
                    #pp.pprint(feature_list)
                    del flist[:]
                    del plot[:]
                    i = 0
                    for item in feature_list:
                        #print(item['properties']['Country'])
                        if item['properties'][field] != '':
                            if minimum_maximum == 'min':
                                if int(item['properties'][field]) >= field_value:
                                    flist.append(item['geometry']['coordinates'])
                            elif minimum_maximum == 'max':
                                if int(item['properties'][field]) <= field_value:
                                    flist.append(item['geometry']['coordinates'])
                    pp.pprint(flist)
                    for item in flist:
                        x = item[0]
                        y = item[1]
                        #y = abs(512 - y)
                        x = mercX(x)
                        y = mercY(y)
                        plotpoint = [int(x),int(y)]
                        plot.append(plotpoint)
                    for p in plot:
                        if min_max_results == 0:
                            pygame.draw.circle(screen, color, p, 3,0)
                        else:
                            if min_max_results > i:
                                pygame.draw.circle(screen, color, p, 3,0)
                                i = i + 1
                else:
                    mx, my = pygame.mouse.get_pos()
                    print (mx, my)
                    my = abs(512 - my)
                    point = toLL((mx,my))
                    print(point) #Getting wrong lon,lat coords
                    vlist = []
                    del vlist[:]
                    elist = []
                    del elist[:]
                    mlist = []
                    del mlist[:]
                    vlist = mh.get_features_near_me('volcanos',point,query_radius)
                    elist = mh.get_features_near_me('earthquakes',point,query_radius)
                    mlist = mh.get_features_near_me('meteorites',point,query_radius)
                    i = 0
                    for x in range(0,3):
                        del flist[:]
                        del plot[:]
                        if x == 0:
                            for item in vlist:
                                flist.append(item['geometry']['coordinates'])
                                color = (255,0,0)
                        elif x == 1:
                            for item in elist:
                                flist.append(item['geometry']['coordinates'])
                                color = (0,0,255)
                        elif x == 2:
                            for item in mlist:
                                flist.append(item['geometry']['coordinates'])
                                color = (0,255,0)
                        for item in flist:
                            x = item[0]
                            y = item[1]
                            #y = abs(512 - y)
                            x = mercX(x)
                            y = mercY(y)
                            plotpoint = [int(x),int(y)]
                            plot.append(plotpoint)
                        for p in plot:
                            if 500 > i:
                                pygame.draw.circle(screen, color, p, 3,0)
                                i = i + 1
                    

        #pygame.image.save(screen,'./screen_shot_query2.png')
        pygame.display.flip()
        pygame.time.wait(5000)