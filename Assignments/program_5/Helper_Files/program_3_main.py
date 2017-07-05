"""
Program:
--------

    Program 3 - DBScan Earthquake Data

Description:
------------
    This program initializes an instance of pygame, and sets forth parameters and variables for
use. It then opens two input files and gathers data from them storing data in list and
dictionary data structures. These input files are created by running, get_quake_points.py, 
adjust_quake_points.py, and find_clusters.py. The dictionary is further adjusted to fit the 
data to the screen. A game loop begins, pushing the background image to the screen, then plotting
points representing earthquakes of 7.0 magnitude or higher at 5 per 30 ms. Once all earthquakes 
have been plotted, minimum bounding rectangles, created by running dbscan from find_clusters.py,
will be plotted with the settings of 15 for epsilon, and 5 for the minimum amount of points.
The time will be adjusted to last slightly longer with the mbr plotted, and a screenshot will be
taken of the final image. The earthquake point incrementer will be reset, and the game loop
will start over as the image populates again.

Name: Matthew Schenk
Date: 22 June 2017
"""



import pygame
import sys,os
import json

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)

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
    pygame.display.set_caption('MBRs')
    screen.fill(background_colour)


    points = []
    pygame.display.flip()
    f = open('./quake_data/quakes-adjusted.json','r')
    points = json.loads(f.read())

    
    f = open('earthquake_clusters.json','r')
    mbr_data = json.loads(f.read())
    mbrs = adjust_location_coords(mbr_data,width,height)

    i = 5
    running = True
    while running:

        screen.blit(bg, (0,0))
        t = 30
        for p in points[:i]:
            pygame.draw.circle(screen, (255,0,0), p, 1,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
        i += 5
        if i >= len(points):
            i = 5
            for id,mbr in mbr_data.items():
                pygame.draw.polygon(screen, (0,255,0), mbr, 2)
                t = 3000
                pygame.image.save(screen,'./screen_shot.png')
        pygame.display.flip()
        pygame.time.wait(t)