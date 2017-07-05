"""
Program:
--------

    Program 5 - Query 1

Description:
------------
    
    This program starts by importing help from other files and libraries. A class is created,
    which allows the MongoDB Server to be accessed by Pymongo, which has various methods for
    gathering data from MongoDB. There is also some defined functions used for plotting onto
    the pygame screen. The program starts by accepting a sys.argv for the radius you would like
    to travel by, it then opens up a pygame screen where you click on or near where you want to
    start your journey and then click once more where or near where you would like to end your
    journey. Due to some performance issues, a screen shot is captured to see the result, as
    well as a text file being generated from the command line that counts down the miles at each 
    airport stop. The finished image has airports in orange with a yellow line connecting them,
    and each airport has volcanos in red, earthquakes in blue, and meteorites in green populated
    due to running a query for those items with the given radius.
    #DISCLAIMER#
    This code can take a second or two to process all of the data, once clicking on your
    destination location, mouse over the close window of the pygame screen it will light
    up and be available to click on and close the window and program when it is finished
    processing the data.

Name: Matthew Schenk
Date: 5 July 2017
"""

import pygame
from pygame.locals import *
import sys,os
import json
import math
from math import radians
from math import sin 
from math import cos
from math import asin
from math import sqrt
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
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        min = 999999
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            d = self._haversine(lon,lat,lon2,lat2)
            if d < min:
                min = d
                print(d)
                print(ap['properties']['ap_name'])
                closest_airp = ap

        return closest_airp

    def destination_in_range(self,lon,lat,r,abr):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        arrive = False
        for ap in air_res:
            if ap['properties']['ap_iata'] == abr:
                print(ap['properties']['ap_name'])
                arrive = True

        return arrive

    def arrive_at_destination(self,lon,lat,r,abr):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        for ap in air_res:
            if ap['properties']['ap_iata'] == abr:
                #print(ap['properties']['ap_name'])
                closest_ap = ap
        print(closest_ap)
        return closest_ap

    def get_farthest_eastern(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        x = 0
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1] 
            if lon2 > lon:
                #d = self._haversine(lon,lat,lon2,lat2)
                d = lon2 - lon
                if d > x:
                    x = d
                    #print(d)
                    #print(ap['properties']['ap_name'])
                    closest_airp = ap

        print(closest_airp)
        return closest_airp
    
    def get_farthest_western(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        x = 0
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1] 
            if lon2 < lon:
                #d = self._haversine(lon,lat,lon2,lat2)
                d = lon - lon2
                if d > x:
                    x = d
                    #print(d)
                    #print(ap['properties']['ap_name'])
                    closest_ap = ap

        print(closest_ap)
        return closest_ap

    def get_farthest_northern(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        y = 0
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1] 
            if lat2 > lat:
                #d = self._haversine(lon,lat,lon2,lat2)
                d = lat2 - lat
                if d > y:
                    x = d
                    #print(d)
                    #print(ap['properties']['ap_name'])
                    closest_ap = ap

        print(closest_ap)
        return closest_ap

    def get_farthest_southern(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        y = 0
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1] 
            if lat2 < lat:
                #d = self._haversine(lon,lat,lon2,lat2)
                d = lat - lat2
                if d > y:
                    x = d
                    #print(d)
                    #print(ap['properties']['ap_name'])
                    closest_ap = ap
        
        print(closest_ap)
        return closest_ap

    def get_closest_to_destination(self,lon,lat,r,dlon,dlat,prev):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        y = 99999999
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1] 
            d = self._haversine(dlon,dlat,lon2,lat2)
            if d < y:
                y = d
                #print(d)
                #print(ap['properties']['ap_name'])
                closest_ap = ap
        
        #print(closest_ap['properties']['city'],', ',closest_ap['properties']['country'])
        #print(closest_ap['properties']['ap_iata'],' is ',d, ' miles away')
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
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r

    def distance_calculator_haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

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


RADIUS_KM = 6371  # in km
RADIUS_MI = 3959  # in mi

def mercX(lon,zoom = 1):
    """
    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return int(a * b)

def mercY(lat,zoom = 1):
    """
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)

def mercToLL(point):
    lng,lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)
    
def toLLtest(point):
    ans = []
    x,y = point
    for i in range(1,5):
        print(i)
        ans.append(mercToLL((x/i,y/i)))
    ans.append(mercToLL((x/4,y)))
    return ans

def toLL(point):
    ans = []
    x,y = point
    y += 256
    return mercToLL((x/4,y/4))

    

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)




if __name__=='__main__':

    pygame.init()
    bg = pygame.image.load("./worldmap.png")

    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query 1')
    screen.fill(background_colour)

    feature = 'airports'
    collection = 'airports'
    #useful airports[properties]: ap_level (lower number is larger), lat, lng, ap_iata: DFW
    #start_point = "DFW"
    #start_point = sys.argv[1]
    #end_point = "MNL"
    #end_point = sys.argv[2]
    radius_query = int(sys.argv[1])
    #radius_query = sys.argv[3]

    mh = mongoHelper()
    airport_start_stop = []
    flist = []
    plot = []

    running = True
    while running:
        screen.blit(bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                print ("MouseClick(X,Y): ",mx, my)
                mx, my = toLL((mx,my))
                print ("Converted: ", mx, my)
                airport_start_stop.append((mx,my))

                if len(airport_start_stop) == 2:
                    starting_airport = mh.get_nearest_neighbor(airport_start_stop[0][0],airport_start_stop[0][1],radius_query)
                    print()
                    print("Your starting airport is: ",starting_airport['properties']['ap_iata'])
                    print()
                    #print(starting_airport)
                    x = mercX(starting_airport['geometry']['coordinates'][0])
                    y = mercY(starting_airport['geometry']['coordinates'][1])
                    plotpoint = [int(x),int(y)-256]
                    pygame.draw.circle(screen, (255,165,0), plotpoint, 1,0)

                    destination_airport = mh.get_nearest_neighbor(airport_start_stop[1][0],airport_start_stop[1][1],radius_query)
                    print()
                    print("Your destination airport is: ", destination_airport['properties']['ap_iata'])
                    print()
                    #print(destination_airport)
                    x = mercX(destination_airport['geometry']['coordinates'][0])
                    y = mercY(destination_airport['geometry']['coordinates'][1])
                    plotpoint = [int(x),int(y)-256]
                    pygame.draw.circle(screen, (255,165,0), plotpoint, 1,0)
                    dest = destination_airport['properties']['ap_iata']
                    #works until here
                    #Iceland at 450 x 20 y
                    #From North/Eastern Canada to Greenland is 934 miles
                    #From Greenland to Iceland is 900 miles
                    #From Brazil to Africa is 1572 miles
                    #To cross Alaska 820 miles
                    #Over 2000 Miles from CA to HI
                    d = mh.distance_calculator_haversine(airport_start_stop[0][0],airport_start_stop[0][1],airport_start_stop[1][0],airport_start_stop[1][1])
                    print("You will be traveling: ",d," miles.")
                
                #Could add in continent string comparisons, to determine if crossing ocean or not//Wrong Idea, changed to better one
                if len(airport_start_stop) == 2:
                    i = 0
                    arrive = mh.destination_in_range(airport_start_stop[0][0],airport_start_stop[0][1],radius_query,dest)
                    x = starting_airport['geometry']['coordinates'][0]
                    y = starting_airport['geometry']['coordinates'][1]
                    dx = destination_airport['geometry']['coordinates'][0]
                    dy = destination_airport['geometry']['coordinates'][1]
                    previous_airport = starting_airport
                    while arrive == False:
                        #Get the next airport and see if it is the destination one
                        next_airport = mh.get_closest_to_destination(x,y,radius_query + i,dx,dy,previous_airport)
                        x = next_airport['properties']['lng']
                        x = float(x)
                        y = next_airport['properties']['lat']
                        y = float(y)
                        arrive = mh.destination_in_range(x,y,radius_query,dest)

                        #Increment Iterator, Plot Previous and Next Airports with Line
                        i = i + 1
                        nx = mercX(next_airport['geometry']['coordinates'][0])
                        ny = mercY(next_airport['geometry']['coordinates'][1])
                        plotpoint = [int(nx),int(ny)-256]
                        px = mercX(previous_airport['geometry']['coordinates'][0])
                        py = mercY(previous_airport['geometry']['coordinates'][1])
                        prevplotpoint = [int(px),int(py)-256]
                        pygame.draw.circle(screen, (255,165,0), plotpoint, 1,0)
                        pygame.draw.line(screen,(255,255,0),prevplotpoint,plotpoint,1)
                        

                        #Check to advance airports
                        if previous_airport['properties']['ap_iata'] != next_airport['properties']['ap_iata']:
                            #if i != 1:
                                #print(i, " is the number of miles appended to the radius before a new airport was found due to map distortion.")
                            print(next_airport['properties']['city'],next_airport['properties']['country'])
                            d = mh.distance_calculator_haversine(x,y,dx,dy)
                            print(next_airport['properties']['ap_iata'],' is ',d, ' miles away')
                            i = 0

                            
                            #Plot Features near Previous Airport Location
                            fex = previous_airport['geometry']['coordinates'][0]
                            fey = previous_airport['geometry']['coordinates'][1]
                            point = (fex,fey)
                            vlist = []
                            del vlist[:]
                            elist = []
                            del elist[:]
                            mlist = []
                            del mlist[:]
                            vlist = mh.get_features_near_me('volcanos',point,radius_query)
                            #pp.pprint(vlist)
                            elist = mh.get_features_near_me('earthquakes',point,radius_query)
                            #pp.pprint(elist)
                            mlist = mh.get_features_near_me('meteorites',point,radius_query)
                            #pp.pprint(mlist)
                            for c in range(0,3):
                                del flist[:]
                                del plot[:]
                                if c == 0:
                                    for item in vlist:
                                        flist.append(item['geometry']['coordinates'])
                                        color = (255,0,0)
                                elif c == 1:
                                    for item in elist:
                                        flist.append(item['geometry']['coordinates'])
                                        color = (0,0,255)
                                elif c == 2:
                                    for item in mlist:
                                        flist.append(item['geometry']['coordinates'])
                                        color = (0,255,0)
                                for item in flist:
                                    fx = item[0]
                                    fy = item[1]
                                    fx = mercX(fx)
                                    fy = mercY(fy)
                                    plotpoint = [int(fx),int(fy)-256]
                                    plot.append(plotpoint)
                                    #print(plotpoint)
                                for p in plot:
                                    pygame.draw.circle(screen, color, p, 1,0)
                            
                            previous_airport = next_airport
                    print("You have arrived at: ", dest)
                    arrival = mh.arrive_at_destination(x,y,radius_query,dest)
                    nx = mercX(arrival['geometry']['coordinates'][0])
                    ny = mercY(arrival['geometry']['coordinates'][1])
                    plotpoint = [int(nx),int(ny)-256]
                    px = mercX(previous_airport['geometry']['coordinates'][0])
                    py = mercY(previous_airport['geometry']['coordinates'][1])
                    prevplotpoint = [int(px),int(py)-256]
                    pygame.draw.circle(screen, (255,165,0), plotpoint, 1,0)
                    pygame.draw.line(screen,(255,255,0),prevplotpoint,plotpoint,1)

                    pygame.image.save(screen,'./screen_shot_query1.png')
                    
                    #Below is hours of work that produced nothing, and then I decided on the above method
                    #This section also calls methods implemented above in mh class
                    #Would love to walk through and pick at the bad logic design
                    '''
                    if airport_start_stop[0][0] < airport_start_stop[1][0]:
                        #travel East
                        x = starting_airport['properties']['lng']
                        x = float(x)
                        y = starting_airport['properties']['lat']
                        y = float(y)
                        arrive = mh.destination_in_range(airport_start_stop[0][0],airport_start_stop[0][1],radius_query,dest)
                        while arrive == False:
                            next_airport = mh.get_farthest_eastern(x,y,radius_query)
                            x = next_airport['properties']['lng']
                            x = float(x)
                            y = next_airport['properties']['lat']
                            y = float(y)
                            arrive = mh.destination_in_range(x,y,radius_query,dest)
                            if x < 0 and y < 60:
                                next_airport = mh.get_farthest_northern(x,y,radius_query*2.5)
                                x = next_airport['properties']['lng']
                                x = float(x)
                                y = next_airport['properties']['lat']
                                y = float(y)
                                arrive = mh.destination_in_range(x,y,radius_query,dest)
                            elif x < 0 and y > 60:
                                next_airport = mh.get_farthest_eastern(x,y,radius_query*2.5)
                                x = next_airport['properties']['lng']
                                x = float(x)
                                y = next_airport['properties']['lat']
                                y = float(y)
                                arrive = mh.destination_in_range(x,y,radius_query,dest)
                            elif y > destination_airport['geometry']['coordinates'][1]:
                                next_airport = mh.get_farthest_southern(x,y,radius_query)
                                x = next_airport['properties']['lng']
                                x = float(x)
                                y = next_airport['properties']['lat']
                                y = float(y)
                                arrive = mh.destination_in_range(x,y,radius_query,dest)
                            elif x < destination_airport['geometry']['coordinates'][0]:
                                next_airport = mh.get_farthest_eastern(x,y,radius_query)
                                x = next_airport['properties']['lng']
                                x = float(x)
                                y = next_airport['properties']['lat']
                                y = float(y)
                            else:
                                next_airport = mh.get_farthest_western(x,y,radius_query)
                                x = next_airport['properties']['lng']
                                x = float(x)
                                y = next_airport['properties']['lat']
                                y = float(y)
                                arrive = mh.destination_in_range(x,y,radius_query,dest)
                        print("You have arrived at: ", dest)
                        arrival = mh.arrive_at_destination(x,y,radius_query,dest)

                    
                    else:
                        #travel West
                        pass
                    '''
        
        pygame.display.flip()
        #pygame.time.wait(5000)
    