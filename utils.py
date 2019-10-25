import png
import numpy
import pprint
import math
import re

def gen_background(width, height, mag, b_col):
    bg = numpy.zeros((width * mag, height * mag, 4), dtype=numpy.uint8)
   
    for y in range(0, height * mag, mag):
        for x in range(0, width * mag):
            bg[y][x] = b_col 
    
    for x in range(0, width * mag, mag):
        for y in range(0, height * mag):
            bg[y][x] = b_col 
    
    for y in range(-1, height * mag, mag):
        if y < 0: continue
        for x in range(0, width * mag):
            bg[y][x] = b_col 
    
    for x in range(-1, width * mag, mag):
        if x < 0: continue
        for y in range(0, height * mag):
            bg[y][x] = b_col

    return bg


class picture(object):
    def __init__(self, width, height):
        self.__array = numpy.full((height,width*4), 220, dtype=numpy.uint8)
        self.__view = self.__array.view().reshape(-1,4)
        self.__width = width
        self.__height = height
        self.__mag = 32
        bg = gen_background(width, height, self.__mag, numpy.array((192, 192, 192, 64), dtype=numpy.uint8))
        self.__dst_rgb = bg[..., :3].astype(numpy.float32) / 255.0

    def put_pixel(self, x, y, color):
        row = y  
        col = x 
        c = numpy.array(color)
        sa_01 = c[3] / 255.0
        o_m_a = 1.0 - sa_01
        sc = c * sa_01 
        idx = self.__width * y + x 
        self.__view[idx] = sc + o_m_a * self.__view[idx]

    def save(self, filename):
        mag = self.__mag

        v = self.__array.view().reshape(self.__height, self.__width, 4)
        a = v.repeat(mag, axis=0).repeat(mag, axis=1)
        
        src_rgb = a[..., :3].astype(numpy.float32) / 255.0
        src_a = a[..., 3].astype(numpy.float32) / 255.0

        out_a = src_a.view()
        out_rgb = (src_rgb * src_a[..., None] + self.__dst_rgb * (1.0 - src_a[..., None]))
        out = numpy.zeros_like(a)
        out[..., :3] = out_rgb * 255
        out[..., 3] = 255
       
        sv = out.view().reshape(self.__height * mag, self.__width * mag * 4)
        png.from_array(sv, mode='RGBA').save(filename)

TRUE_RE = re.compile(".*True.*")

def load_map(filename, canvas_size):
    c_width, c_height = canvas_size

    player_pos = (0,0)
    enemy_pos = (0,0)
    expected_result = False

    lines = None 

    with open(filename, "r") as f:
        lines = f.readlines()

    expected_result = TRUE_RE.match(lines[0]) is not None
    lines = lines[1:]

    height = len(lines)
    width = max([len(w.rstrip("\n")) for w in lines])

    if height > c_height:
        print("Map {0} height dimension doesn't fit the canvas!".format(filename))
        exit(1)

    if width > c_width:
        print("Map {0} width dimenstion doesn't fit the canvas!".format(filename))
        exit(1)

    # let's calculate canvas padding
    x_pad = (c_width - width) // 2
    y_pad = (c_height - height) // 2

    m = numpy.zeros((c_height,c_width),numpy.uint8)

    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c == "\n":
                continue
            if c == "#":
                m[y+y_pad][x+x_pad] = 1
            if c == "@":
                m[y+y_pad][x+x_pad] = 2
                player_pos = (x+x_pad,y+y_pad)
            if c== "h":
                m[y+y_pad][x+x_pad] = 3
                enemy_pos = (x+x_pad,y+y_pad)

    return (m,player_pos,enemy_pos,expected_result,width,height)

def draw_map(m,p):
    for y,r in enumerate(m):
        for x,c in enumerate(r):
            if c == 1:
                p.put_pixel(x,y,(64, 64, 64, 220)) 
            if c == 2:
                p.put_pixel(x,y,(0, 255, 0, 220))
            if c == 3:
                p.put_pixel(x,y,(255, 0, 0, 220))

def draw_route(route,p,c):
    for e in route:
        x,y = e
        p.put_pixel(x,y,c)
