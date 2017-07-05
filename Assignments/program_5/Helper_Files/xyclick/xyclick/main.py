
import pygame
from pygame.locals import *
import json
import os,sys
import math 

"""
This example based on a 1024x512 screen size. If you screen size is different, then 
you need to adjust. Mercator expects 1024x768 ratio (I'm pretty sure) that's why
I subtract 256 from the 'y' before I plot it. So you need to add that back to the 
'y' when you get a Lon/Lat. 
"""

BASE = os.path.dirname(os.path.realpath(__file__))

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

    background_colour = (255,255,255)
    black = (0,0,0)
    (screen_width, screen_height) = (1024, 512)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Simple Map')

    bg = pygame.image.load(os.path.join(BASE,"1024x512.png"))

    screen = pygame.display.set_mode((screen_width,screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
    screen.blit(pygame.transform.scale(bg,(screen_width,screen_height)), (0, 0))

    pygame.draw.circle(screen,(255,0,0),(int(mercX(131.6)),int(mercY(34.5))-256),2,0)
    pygame.draw.circle(screen,(255,0,0),(int(mercX(140.29)),int(mercY(37.64))-256),2,0)
    pygame.draw.circle(screen,(255,0,0),(int(mercX(139.2)),int(mercY(36.56))-256),2,0)
    pygame.draw.circle(screen,(255,0,0),(mercX(-98.5034180),mercY(33.9382331)-256),2,0)
    pygame.time.wait(1000)

    pygame.display.flip()


    while True:
        pygame.event.pump()
        event = pygame.event.wait()
        if event.type == MOUSEBUTTONUP:
            print(event.pos)
            x,y = event.pos
            print(toLL((x,y)))

        

        pygame.display.flip()

        if event.type == QUIT:
            pygame.display.quit()
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            screen.blit(pygame.transform.scale(bg, event.dict['size']), (0, 0))
