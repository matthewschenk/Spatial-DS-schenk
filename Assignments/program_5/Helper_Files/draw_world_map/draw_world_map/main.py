import os,sys
import math
import pygame
from pygame.locals import *
from pymongo import MongoClient
from map_icons import map_icon
from mongo_helper import MongoHelper
from map_helper import *
from color_helper import ColorHelper

#http://cs.mwsu.edu/~griffin/geospatial/

BASE = os.path.dirname(os.path.realpath(__file__))

class PygameHelper(object):
    def __init__(self,width,height):
        self.screen_width = width
        self.screen_height = height
        self.keyval = 1000

        self.bg = pygame.image.load(os.path.join(BASE,"images/2048x1024.png"))

        self.polygons = []             # any polygon to be drawn
        self.points = []               # any point to be drawn

        self.map_event_functions = {}

        pygame.init()
        self.game_images = {}

    def Capture(self,name,pos,size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.screen,(0,0),(pos,size))  # Blit portion of the display to the image
        pygame.image.save(image,name)  # Save the image to the disk
        
    def load_image(self,key,path,coord):
        """
        Params:
            key: name to reference image with
            path: path to image 
            coord: location to place image on screen
        """
        self.game_images[key] = {'pyg_image':pygame.image.load(path),'coord':coord}

    def adjust_point(self,p,icon=None):
        if icon:
            size = self._get_icon_size(icon)
            voffset = size
            hoffset = size//2
        else:
            voffset = 0
            hoffset = 0

        lon,lat = p
        x = (mercX(lon) / 1024 * self.screen_width) - hoffset
        scale = 1 / math.cos(math.radians(lat))             # not used
        y = (mercY(lat) / 512 * self.screen_height) - (self.screen_height/2) - voffset
        return (x,y)

    def add_polygon(self,polygon,color,width):
        """
        Add polygons to local list to be drawn
        """
        outofrange = [-180, -90, 180, 90]
        adjusted = []
        for p in polygon[0]:
            if math.floor(p[0]) in outofrange or p[1] in outofrange:
                continue
            adjusted.append(self.adjust_point(p))
        self.polygons.append({'poly':adjusted,'color':color,'width':width})

    def add_points(self,point,icon):
        """
        Add points to local list to be drawn
        """
        if type(point) is list:
            for p in point:
                coord = self.adjust_point(p,icon)
                self.load_image(self._unique_key(), icon, coord)

    def draw_polygons(self):
        for poly in self.polygons:
            if len(poly['poly']) < 3:
                continue
            pygame.draw.polygon(self.screen,poly['color'],poly['poly'],poly['width'])

    def add_event_function(self,type,fun):
        if not type in self.map_event_functions:
            self.map_event_functions[type] = []
        self.map_event_functions[type].append(fun)

    def start_display(self):
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.blit(pygame.transform.scale(self.bg,(self.screen_width,self.screen_height)), (0, 0))

        for key,image in self.game_images.items():
            self.screen.blit(image['pyg_image'],image['coord'])

        pygame.display.flip()

        while True:
            pygame.event.pump()
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONUP:
                pass
            if event.type == KEYUP:
                if event.key == 273:
                    pass
                if event.key == 274:
                    pass

            self.draw_polygons()
            pygame.display.flip()
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.screen.blit(pygame.transform.scale(self.bg, event.dict['size']), (0, 0))
                for key,image in self.game_images.items():
                    self.screen.blit(image['pyg_image'],image['coord'])
                pygame.display.flip()

    def _unique_key(self):
        key = self.keyval
        self.keyval += 1
        return key

    def _get_icon_size(self,icon):
        return int(icon.split('/')[-2].split('x')[0])

class MapFacade(object):
    def __init__(self,width,height):
        self.screen_width = width
        self.screen_height = height
        self.mh = MongoHelper()
        self.pyg = PygameHelper(width,height)
    
    def run(self):
        self.pyg.start_display()

    def draw_country(self,codes,color=(255,168,0),width=1):
        for code in codes:
            country = self.mh.get_country_poly(code)
            if country is not None:
                break

        if country['type'] == 'MultiPolygon':
            for polygon in country['coordinates']:
                self.pyg.add_polygon(polygon,color,width)
        else:
            self.pyg.add_polygon(country['coordinates'],color,width)


    def draw_airports(self,icon):
        airports = self.mh.get_all('airports')
        points = []
        for ap in airports:
            points.append(ap['geometry']['coordinates'])
        self.pyg.add_points(points,icon)

    def pin_the_map(self,points,icon):
        self.pyg.add_points(points,icon)

    def draw_all_countries(self,border=0):
        c  = ColorHelper()
        unique_list = []
        for i in range(14):
            unique_list.append(c.get_unique_random_color())

        
        countries = self.mh.get_all('countries',{},{'_id':0,'properties.MAPCOLOR13':1,'properties.ISO_A3':1,'properties.ADM0_A3_US':1, 'properties.SU_A3':1, 'properties.GU_A3':1})
        for country in countries:
            codes = []
            color = int(country['properties']['MAPCOLOR13'])-1
            for c in ['ISO_A3','ADM0_A3_US','SU_A3','GU_A3']:
                if not str(c) == '-99':
                    codes.append(country['properties'][c])
            if color < 0:
                color = 13
            self.draw_country(codes,unique_list[color],border)

screen_width = 2048
screen_height = 1024

mf = MapFacade(screen_width,screen_height)
mf.pin_the_map( [[131.6,34.5],[140.29,37.64],[139.2,36.56]],map_icon('Centered','Pink',32,''))
mf.pin_the_map([[-98.5034180,33.9382331]],map_icon('Centered','Pink',32,''))
# mf.draw_country('BRA')
# mf.draw_country('GRL')
# mf.draw_country('RUS')
# mf.draw_country('FRA',(199,21,133),0)
# mf.draw_country('NOR',(21,199,133),0)
mf.draw_all_countries(1)
mf.draw_airports(map_icon('Centered','Azure',16,''))

mf.run()
