import pygame
import random
from dbscan import *
import sys,os
import pprint as pp

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

print('Matthew Schenk')
print('CMPS 5323 - Dr. Griffin')
print('Program 2: NYC Crime')


def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    mbrs = []
    clusters =  dbscan(points, epsilon, min_pts)

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs) 
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """
    for id in range(len(clusters)-1):
        xs = []
        ys = []
        for p in clusters[id]:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs) 
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)
        mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    return mbrs


def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

def populate_burrow(burrow):
    """
    This will accept a burrow, and populate a list of tuples where crimes have occured.
    ARGS: string
    RET: list
    """
    points = []
    adjustedpoints = []
    keys = []
    crimes = []
    got_keys = False

    #This code opens up filtered files and stores them in list crimes, by line to keep everything parallel
    with open(burrow) as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                #print(keys)
                got_keys = True
                continue

            crimes.append(line)
    print('Finished Reading in Crime Data for '+burrow)

    #Loop to traverse through and set min/max x,y values
    minx = 100000000
    miny = 100000000
    maxx = -100000000
    maxy = -100000000
    counter = 1
    for crime in crimes:
        #print(crime[19],crime[20])
        #print(counter)
        #counter += 1
        #Found Error on Line 6587 in Brooklyn File, removed as no lat/long or x,y provided
        #Found Error on Line 4438 in Bronx File, removed
        #Found Error on Line 5443 in Manhattan File, removed
        x = float(crime[19])/1000
        y = float(crime[20])/1000
        y = abs(y - 700)
        if minx > x:
            minx = x
        if miny > y:
            miny = y
        if maxx < x:
            maxx = x
        if maxy < y:
            maxy = y
        points.append((int(x),int(y)))
    #print(points)

    #Code for adjusting points for scaling, and appending to points list
    #Possible to access tuples in append[], and then amend instead of using crime again
    #Above line is incorrect, tuples are immutable
    for item in points:
        x,y = item
        x = (x - 913.46)/(1067.186 - 913.46)
        x =  x * 1000
        y = (y - 428.18)/(578.688 - 428.18)
        y = y * 1000
        adjustedpoints.append((int(x),int(y)))
    #print(points)
    #print(minx)
    #print(maxx)
    #print(miny)
    #print(maxy)

    print('Finished Appending List for '+burrow)
    return adjustedpoints



background_colour = (255,255,255)
black = (0,0,0)
(width, height) = (1000, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('NYC Crime')
screen.fill(background_colour)

pygame.display.flip()

epsilon = 0.5
min_pts = 3.0

#Code for populating the five burrows
bronx = 'filtered_crimes_bronx.csv'
bronx_crimes = []
bronx_crimes = populate_burrow(bronx)

brooklyn = 'filtered_crimes_brooklyn.csv'
brooklyn_crimes = []
brooklyn_crimes = populate_burrow(brooklyn)

manhattan = 'filtered_crimes_manhattan.csv'
manhattan_crimes = []
manhattan_crimes = populate_burrow(manhattan)

queens = 'filtered_crimes_queens.csv'
queens_crimes = []
queens_crimes = populate_burrow(queens)

staten_island = 'filtered_crimes_staten_island.csv'
staten_island_crimes = []
staten_island_crimes = populate_burrow(staten_island)

#testing points and overwriting
points = manhattan_crimes
#mbrs = calculate_mbrs(points, epsilon, min_pts)

running = True
while running:

    for p in points:
        #Add if/elif statement to print dots in colors here, by traversing crime in crimes and using crime['crimename']
        #for crime in crimes:
        #if crime[?] == 'LARCENY', elif 'ASSAULT', elif 'HARRASSMENT', elif 'DRUGS', elif 'VEHICLE FRAUD'
        #or use dictionary when reading from files containing key as (x,y) with values crimename and color set to crimename
        #then can traverse through dictionary here, and just pass in the color name with the set coord key
        pygame.draw.circle(screen, black, p, 1, 0)
    for c in bronx_crimes:
        pygame.draw.circle(screen, (2,120,120), c, 2, 0)
    for c in brooklyn_crimes:
        pygame.draw.circle(screen, (128,22,56), c, 2, 0)
    for c in manhattan_crimes:
        pygame.draw.circle(screen, (194,35,38), c, 2, 0)
    for c in queens_crimes:
        pygame.draw.circle(screen, (243,115,56), c, 2, 0)
    for c in staten_island_crimes:
        pygame.draw.circle(screen, (253,182,50), c, 2, 0)
    #for mbr in mbrs:
    #    pygame.draw.polygon(screen, black, mbr, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.image.save(screen, DIRPATH+'/'+'all_buroughs_screen_shot.png')
        if event.type == pygame.MOUSEBUTTONDOWN:
            clean_area(screen,(0,0),width,height,(255,255,255))
            points.append(event.pos)
            mbrs = calculate_mbrs(points, epsilon, min_pts)
    pygame.display.flip()