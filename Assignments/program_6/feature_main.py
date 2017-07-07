"""
Program:
--------

    Program 6 - Heat Map with Terrorisms

Description:
------------
    DESIGNED TO WORK WITH ANY COLLECTION!
    Call from command line: python feature_main.py [feature]
    where [feature] = collection name
    For example: volcanos, earthquakes, meteorites

    This program starts by importing various libraries for aid, some include
    pygame and pymongo. A class is created to help create a link between
    our program and the MongoDB server on the laptop, which is where it will
    pull the data from. Functions provided for scaling lon/lat into x,y
    coordinates follows after that, with methods that can utilize clustering and
    DBScan after them. A method that will return a blend of RGB values on a scale
    is after that.
    In the main program, it will start by creating a pygame instance and screen
    setting the variables, which include size, background, and screen title. Feature
    is defined as 'terrorism' though could be augmented to become a sys.argv in future
    implementation. Declare an instance of our Mongohelper class, and lists to call
    the function that will return all information in our data base on our selected
    feature, which will then be processed to store adjusted lon/lat coordinates into
    x,y coordinates in a list. The x,y list is traversed, onto a 2D grid or matrix
    and each index that corresponds to the x,y list is updated by 10, when an index
    becomes greater than 300 (30 attacks on same location) the two outer rings are
    also updated with 8 and 6 respectively, creating more visualization for higher
    attack areas.
    Followed by a dictionary which was our first implementation, storing 10 per unique
    attack location. This dictionary is traversed finding both the minimum and maximum
    amounts for location attacked. However, after iteration minimum will be one, and the
    maximum must be larger than the number of steps(unique attacks) used for color 
    scaling for our implementation to work correctly, the maximum being 256 cubed. It is
    then sorted, and can be used if the drawing loops in the pygame loop are switched.
    Colors are scaled according to steps, which is the number of unique attacks (2627) which
    is in the code following. These colors are stored in a list of colors when they are being
    created.
    Two dictionary's are declared next, one being filled by traversing the 2D grid, and looking
    for unique attack numbers for every location. Everytime a new key is created, the counter
    increments which returns the number of unique attack numbers. The dictionary is then sorted,
    and traversed while it's keys are being updated with colors from the colorlist, as well as,
    the second dictionary having keys created with colors as their values, equally two identical
    dictionaries.
    The game loop then begins, applying the background image and setting a pause time. THe 2DGrid
    is traversed plotting each point above 0, as all cells with 0 will result in an almost entirely
    blue printout. Cells are then assigned a color by traversing the dictionary and pulling the
    assigned color for that unique attack number they hold. Then given the information required
    pygame draws a small circle on the screen, resulting in a heat map like image. As the circles
    are larger than pixels which are grid consists of, and the last item to be drawn is always 
    placed on top and over existing items.


Name: Matthew Schenk, Abdel Aitroua, Tanaka Madyara
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
import collections

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

    # [feature] [grid_width] [grid_height]
    # [terrorism]
    feature = sys.argv[1]
    
    #For Clustering, maybe
    #w = int(sys.argv[1])
    #h = int(sys.argv[2])

    mh = mongoHelper()
    flist = []  
    plot = []
    magquake = []

    #Gather all data for feature
    feature_list = mh.get_all(feature)
    #Append List of Coordinates
    for item in feature_list:
        #if item['geometry']['coordinates'] != None:
        flist.append(item['geometry']['coordinates'])
        if feature == 'earthquakes':
            magquake.append(item['properties']['mag'])
    #Adjust Coordinate List
    for item in flist:
        x = mercX(item[0])
        y = mercY(item[1])
        plotpoint = [int(x),int(y)-256]
        #print(plotpoint)
        if plotpoint[1] >= 0:
            plot.append(plotpoint)
        #print(plotpoint)

    '''
    #Testing Data Points
    #Found bad point at [674,-71]
    
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
    grid = [[0 for a in range(h)] for b in range(w)]
    #Testing
    #print("grid 0,0 = ",grid[0][0])
    #print("grid 50,250 = ",grid[50][250])
    #print("grid 0,0 = ",grid[0][0] + 1)
    
    quakercounter = 0
    for p in plot:
        x,y = p
        if x <= 1024 and y <= 512:
            if x >= 0 and y >= 0:
                grid[x][y] = grid[x][y] + 10.0 * magquake[quakercounter]
                quakercounter += 1
                if grid[x][y] > 300:
                    grid[x-1][y-1] += 8.0
                    grid[x][y-1] += 8.0
                    #Have to comment out x+1 x+2 as earthquakes are on edge of map/grid
                    #grid[x+1][y-1] += 8.0
                    #grid[x+1][y] += 8.0
                    #grid[x+1][y+1] += 8.0
                    grid[x][y+1] += 8.0
                    grid[x-1][y+1] += 8.0
                    grid[x-1][y] += 8.0

                    grid[x-2][y-2] += 6.0 
                    grid[x-1][y-2] += 6.0
                    grid[x][y-2] += 6.0
                    #grid[x+1][y-2] += 6.0
                    #grid[x+2][y-2] += 6.0
                    #grid[x+2][y-1] += 6.0
                    #grid[x+2][y] += 6.0
                    #grid[x+2][y+1] += 6.0
                    #grid[x+2][y+2] += 6.0
                    #grid[x+1][y+2] += 6.0
                    grid[x][y+2] += 6.0
                    grid[x-1][y+2] += 6.0 
                    grid[x-2][y+2] += 6.0
                    grid[x-2][y+1] += 6.0
                    grid[x-2][y] += 6.0
                    grid[x-2][y-1] += 6.0

                #Above was always returning:     #grid[x][y] = grid[x][y] + 1
                                                 #IndexError: list index out of range
                                                 #Returned because had w and h backwards.


    #Dictionary Implementation
    new_grid = {}
    for p in plot:
        (x,y) = p
        key = (x,y)
        if not key in new_grid:
            new_grid[key] = 0.0
        new_grid[key] += 10.0
        
    '''
    Traverse dictionary
    '''
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
    maxterror = 1200000

    sorted_x = sorted(new_grid.items(), key=operator.itemgetter(1))
    #pp.pprint(sorted_x)

    #Create and Update two dictionary's with keys as unique attack numbers with RGB values
    count = {}
    colorcount = {}
    counter = 0
    for i in range(len(grid)):
            for j in range(len(grid[0])):
                key = grid[i][j]
                if not key in count:
                    count[key] = (0,0,0)
                    counter += 1
    print(counter)
    #print("Count DICT:")
    #pp.pprint(count)


    #Code to scale the colors and store them in a list of colors
    steps = counter
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

    counter = 0
    for key in sorted(count):
        colorcount[key] = colorslist[counter]
        count[key] = colorslist[counter]
        counter += 1
    #print("ColorCount DICT:")
    #pp.pprint(colorcount)
    #print("Count DICT:")
    #pp.pprint(count)

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
        '''
        #MUST CHANGE STEPS IN COLORS FUNCTION TO 100 TO UTILIZE SCALING % COLORS
        #BASED ON A HARD LIMIT SET WITH MAXTERROR: 500 or 1000
        for data in sorted_x:
            #print(data)
            k,v = data
            #print(k)
            #print(v)
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
        '''
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                col = grid[i][j]
                colour = colorcount[col]
                p = [i,j]
                if colour != (0,0,255):
                    pygame.draw.circle(screen, colour, p, 1,0)
        pygame.image.save(screen,'./screen_shot_program6_'+feature+'.png')


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
        pygame.display.flip()
        pygame.time.wait(t)
        
