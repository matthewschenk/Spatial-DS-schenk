"""
Program:
--------

    Program 5 - Query 3

Description:
------------
    
    This program starts by importing help from other files and libraries. A class is created,
    which allows the MongoDB Server to be accessed by Pymongo, which has various methods for
    gathering data from MongoDB. There is also some defined functions used for plotting onto
    the pygame screen. The program starts by accepting a system arguement for the desired
    feature to be displayed. All volcanos in red, earthquakes in blue, or meteorites in green
    from the database are displayed across the entire pygame screen, where three bounding 
    rectangles surround the three most highly clustered or populated areas.
    #DISCLAIMER#
    In my testing, only the volcanos would appear on my laptop. Issues for this I think is
    that the amount of data to be processed by DBScan for clustering on earthquakes and
    meteorites is perhaps too much. As we had run into similar issues when clustering NYC
    crime data. When attempting to run these pygame would eventually return "Not Responding"
    and would have to be forcibly closed.

Name: Matthew Schenk
Date: 5 July 2017
"""

import pygame
from pygame.locals import *
import sys,os
import json
import math
from pymongo import MongoClient
import pprint as pp
from dbscan import *

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

    def get_all(self,collection):
        res = self.client['world_data'][collection].find()
        return self._make_result_list(res)

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

def calculate_mbrs(points, epsilon, min_pts,debug=False):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = {}
    clusters =  dbscan(points, epsilon, min_pts,debug=debug)
    extremes = {'max_x':sys.maxsize * -1,'max_y':sys.maxsize*-1,'min_x':sys.maxsize,'min_y':sys.maxsize}

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """

    for id,cpoints in clusters.items():
        print(id)
        xs = []
        ys = []
        for p in cpoints:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        if max_x > extremes['max_x']:
            extremes['max_x'] = max_x
        if max_y > extremes['max_y']:
            extremes['max_y'] = max_y
        if min_x < extremes['min_x']:
            extremes['min_x'] = min_x
        if min_y < extremes['min_y']:
            extremes['min_y'] = min_y

        mbrs[id]=[(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)]
    mbrs['extremes'] = extremes
    return mbrs

def adjust_location_coords(mbr_data,width,height):
    """
    Adjust your point data to fit in the screen. 
    Expects a dictionary formatted like `mbrs_manhatten_fraud.json` with extremes in it.
    """
    maxx = float(mbr_data['extremes']['max_x']) # The max coords from bounding rectangles
    minx = float(mbr_data['extremes']['min_x'])
    maxy = float(mbr_data['extremes']['max_y'])
    miny = float(mbr_data['extremes']['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = {}

    del mbr_data['extremes']

    for id,mbr in mbr_data.items():
        adjusted[id] = []
        for p in mbr:
            x,y = p
            x = float(x)
            y = float(y)
            xprime = (x - minx) / deltax         # val (0,1)
            yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
            adjx = int(xprime*width)
            adjy = int(yprime*height)
            adjusted[id].append((adjx,adjy))
    return adjusted


if __name__=='__main__':

    pygame.init()
    bg = pygame.image.load("./worldmap.png")

    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query 3')
    screen.fill(background_colour)

    # [feature] [min_pts] [eps]
    #Volcanos, Earthquakes, Meteorites
    feature = sys.argv[1]
    if feature == 'volcanos':
        color = (255,0,0)
    elif feature == 'earthquakes':
        color = (0,0,255)
    elif feature == 'meteorites':
        color = (0,255,0)

    min_pts = int(sys.argv[2])
    eps = int(sys.argv[3])

    mh = mongoHelper()
    flist = []  
    plot = []

    #Gather all data for feature
    feature_list = mh.get_all(feature)
    #Append List of Coordinates
    for item in feature_list:
        #if item['geometry']['coordinates'] != None:
        flist.append(item['geometry']['coordinates'])
    #Adjust Coordinate List
    for item in flist:
        x = mercX(item[0])
        y = mercY(item[1])
        plotpoint = [int(x),int(y)-256]
        #print(plotpoint)
        plot.append(plotpoint)
    
    # Find the clusters from our data files
    mbr_data = calculate_mbrs(plot,eps,min_pts,debug=True)

    # Remove the cluster that contains all the points NOT in a cluster
    del mbr_data[-1]
    
    '''
    #Below Not Needed, already adjusted data!!!!!
    mbrs = adjust_location_coords(mbr_data,width,height)
    '''
    
    #Find top three biggest rectangles
    bronze = []
    big = 0
    silver = []
    bigger = 0
    gold = []
    biggest = 0
    topmbrs = {}
    for k,v in mbr_data.items():
        print(k)
        print(v)
        if k != 'extremes':
            x1 = v[0][0]
            y1 = v[0][1]
            x2 = v[1][0]
            y2 = v[2][1]
            #print(x1,x2)
            #print(y1,y2)
            x = abs(x1 - x2)
            y = abs(y1 - y2)
            #print(x,y)
            area = x * y
            print(area)
            if area >= biggest:
                biggest = area
                gold = v
            elif area >= bigger:
                bigger = area
                silver = v
            elif area >= big:
                big = area
                bronze = v
    topmbrs['0'] = gold
    topmbrs['1'] = silver
    topmbrs['2'] = bronze

    print(gold)
    print(silver)
    print(bronze)


    running = True
    while running:
        screen.blit(bg, (0,0))
        for p in plot:
            pygame.draw.circle(screen, color, p, 1,0)
        
        #for id,mbr in mbr_data.items():
        for id,mbr in topmbrs.items():
            pygame.draw.polygon(screen, (255,255,0), mbr, 2)
            t = 3000
            pygame.image.save(screen,'./screen_shot_query3.png')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
        pygame.time.wait(t)
        
