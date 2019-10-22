import png
import numpy
import pprint
import math
import re

class picture(object):
    def __init__(self, width, height, pixel_size = 1):
        self.__array = numpy.full((height,width*4), 255, dtype=numpy.uint8)
        self.__view = self.__array.view().reshape(-1,4)
        self.__widht = width
        self.__heihgt = height
        self.__pixel_size = pixel_size

    def put_pixel(self, x, y, color):
        row = y * self.__pixel_size 
        col = x * self.__pixel_size
        c = numpy.array(color)
        sa_01 = c[3] / 255.0
        o_m_a = 1.0 - sa_01
        sc = c * sa_01 
        for yy in range(row, row + self.__pixel_size):
            index = self.__widht * yy 
            for xx in range(col, col + self.__pixel_size):
                idx = index + xx
                self.__view[idx] = sc + o_m_a * self.__view[idx]

    def save(self, filename):
        png.from_array(self.__array, mode='RGBA').save(filename)

TRUE_RE = re.compile(".*True.*")

def load_map(filename):
    m = numpy.zeros((16,16),numpy.uint8)
    player_pos = (0,0)
    enemy_pos = (0,0)
    expected_result = False
    with open(filename, "rb") as f:
        for y,l in enumerate(f.readlines()):
            if y == 0:
                expected_result = TRUE_RE.match(l.decode("utf-8")) is not None
                continue
            for x,c in enumerate(l.decode("utf-8")):
                if c == "\n":
                    continue
                if c == "#":
                    m[y][x] = 1
                if c == "@":
                    m[y][x] = 2
                    player_pos = (x,y)
                if c== "h":
                    m[y][x] = 3
                    enemy_pos = (x,y)

    return (m,player_pos,enemy_pos,expected_result)

def draw_map(m,p):
    for y,r in enumerate(m):
        for x,c in enumerate(r):
            if c == 1:
                p.put_pixel(x,y,(0, 0, 0, 255)) 
            if c == 2:
                p.put_pixel(x,y,(0, 255, 0, 255))
            if c == 3:
                p.put_pixel(x,y,(255, 0, 0, 255))

def draw_route(route,p):
    for e in route:
        x,y = e
        p.put_pixel(x,y,(255,0,255,128))
