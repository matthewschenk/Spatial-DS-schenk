"""
Program:
--------

    Program 6 - Heat Map with Terrorisms

Description:
------------

    Runs our first iteration of program 6, using dictionary and colorlist.
    The colors are scaled to 100, and then points are scaled as a percentage
    of the set maximum, in the end showing more Red spots as there is more
    than one spot with 100%, but gives a decent picture.
    

Name: Matthew Schenk
Date: 7 July 2017
"""

import pygame
from pygame.locals import *
import sys,os
import json
import math
from pymongo import MongoClient
import pprint as pp
from dbscan import *
import operator

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

EPSILON = sys.float_info.epsilon  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))



if __name__=='__main__':

    pygame.init()
    bg = pygame.image.load("./worldmap.png")

    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024, 512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Reported World Terror')
    screen.fill(background_colour)

    # [feature] [min_pts] [eps]
    # [terrorism] [pass in parameters for size of array?]
    feature = 'terrorism'
    
    #For Clustering, maybe
    #w = int(sys.argv[1])
    #h = int(sys.argv[2])

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
        if plotpoint[1] >= 0:
            plot.append(plotpoint)
        #print(plotpoint)

    #Testing Data Points
    #Found bad point at [674,-71]
    '''
    for p in plot:
        x,y = p
        if x >= 1024:
            print(p)
        if y >= 512:
            print(p)
        if x <= 0:
            print(p)
        if y <= 0:
            print(p)
    '''

    #Create 2D Grid and Populate
    w, h = 1025, 513
    grid = [[0 for a in range(w)] for b in range(h)]
    #Testing
    #print("grid 0,0 = ",grid[0][0])
    #print("grid 50,250 = ",grid[50][250])
    #print("grid 0,0 = ",grid[0][0] + 1)
    '''
    for p in plot:
        x,y = p
        if x <= 1024 and y <= 512:
            if x >= 0 and y >= 0:
                grid[x][y] = grid[x][y] + 1
                #Above is always returning:     grid[x][y] = grid[x][y] + 1
                                                IndexError: list index out of range

    '''

    new_grid = {}
    for p in plot:
        (x,y) = p
        key = (x,y)
        if not key in new_grid:
            new_grid[key] = 0
        new_grid[key] += 1
        
    
    #print(new_grid) 
    minterror = 100000000
    maxterror = 0
    for k, v in new_grid.items():
        #print(k, v) #(x,y) v
        if v > maxterror:
            maxterror = v
        if v < minterror:
            minterror = v
    print(minterror)
    print(maxterror)
    print(len(new_grid))
    maxterror = 50

    sorted_x = sorted(new_grid.items(), key=operator.itemgetter(1))
    pp.pprint(sorted_x)

    steps = 100
    colorslist = []
    delta = float(maxterror-minterror) / steps
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    print('  Val       R    G    B')
    for i in range(steps+1):
        val = minterror + i*delta
        r, g, b = convert_to_rgb(minterror, maxterror, val, colors)
        print('{:.3f} -> ({:3d}, {:3d}, {:3d})'.format(val, r, g, b))
        colorslist.append((r,g,b))
    #print(colorslist)

        

        

    
    '''
    #If wanting to try clusters later
    # Find the clusters from our data files
    #mbr_data = calculate_mbrs(plot,eps,min_pts,debug=True)

    # Remove the cluster that contains all the points NOT in a cluster
    #del mbr_data[-1]
    
    
    #Below Not Needed, already adjusted data!!!!!
    mbrs = adjust_location_coords(mbr_data,width,height)
    '''


    running = True
    while running:
        screen.blit(bg, (0,0))
        t = 3000
        for data in sorted_x:
            print(data)
            k,v = data
            print(k)
            print(v)
            #for z,o in k:
                #print(z)
                #x,y = z
            p = [k[0],k[1]]
            
            col = v/maxterror * 100
            if col >= 100:
                col = 100
            colour = colorslist[int(col)]
            pygame.draw.circle(screen, colour, p, 1,0)
        pygame.image.save(screen,'./screen_shot_program6.png')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
        pygame.time.wait(t)
        
