import math
from enum import Enum

class dda_dir(Enum):
    DDA_NONE = 0
    DDA_X  = 1
    DDA_Y  = 2
    DDA_XY = 3

class dda_data(object):
    __slots__ = ['x0', 'y0', 'dx', 'dy', 'odx', 'ody', 'step', 'd_dir']
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0

        dx = x1 - x0
        dy = y1 - y0 

        self.odx = dx
        self.ody = dy

        step = 0
        d_dir = dda_dir.DDA_NONE

        adx = abs(dx)
        ady = abs(dy)

        if adx > ady:
            step = adx
            d_dir = dda_dir.DDA_X 
        elif adx < ady:
            step = ady
            d_dir = dda_dir.DDA_Y
        else:
            step = adx
            d_dir = dda_dir.DDA_XY

        if step == 0:
            self.dx = 0
            self.dy = 0
            self.step = 0
            self.d_dir = d_dir
            return

        dx = dx / step
        dy = dy / step

        self.dx = dx
        self.dy = dy
        self.step = step
        self.d_dir = d_dir 
    
    def calc_pos(self, i):
        x = round(self.x0 + i * self.dx)
        y = round(self.y0 + i * self.dy)
        return (x,y)

    def calc_floor_pos(self,i):
        x = math.floor(self.x0 + i * self.dx)
        y = math.floor(self.y0 + i * self.dy)
        return (x,y)

    def calc_ceil_pos(self,i):
        x = math.ceil(self.x0 + i * self.dx)
        y = math.ceil(self.y0 + i * self.dy)
        return (x,y)

def sign( x ):
    if x == 0:
        return 0
    return 1 if x > 0 else -1

def is_move_valid(dda, x0, y0, x1, y1):
    dif_x = abs(x1 - x0)
    dif_y = abs(y1 - y0)
    
    if dif_x > 1 or dif_y > 1:
        return False

    inc_x = abs(x1 - x0) == 1
    inc_y = abs(y1 - y0) == 1

    if inc_x and inc_y:
        return True

    if inc_x and dda.d_dir == dda_dir.DDA_X:
        return True

    if inc_y and dda.d_dir == dda_dir.DDA_Y:
        return True

    return False

def trace_line(m, x0, y0, x1, y1):
    ret = []

    dda = dda_data(x0, y0, x1, y1)
    orig_dda = dda
    i = 1
    prevx = x0
    prevy = y0
    
    while( True ):
        x_f, y_f = dda.calc_floor_pos(i)
        x_r, y_r = dda.calc_pos(i)
        x_c, y_c = dda.calc_ceil_pos(i)
        
        # Pick one of three options for rounding
        r_valid = m[y_r][x_r] != 1
        c_valid = m[y_c][x_c] != 1
        f_valid = m[y_f][x_f] != 1

        if r_valid:
            x, y = x_r, y_r
        elif f_valid and c_valid:
            f_dist = abs(x1 - x_f) + abs(y1 - y_f)
            c_dist = abs(x1 - x_c) + abs(y1 - y_c)
            
            print(f_dist, c_dist)

            if f_dist < c_dist:
                x, y = x_f, y_f
            else:
                x, y = x_c, y_c
        elif f_valid:
            x, y = x_f, y_f
        elif c_valid:
            x, y = x_c, y_c
        else:
            return (ret, False)
        
        # Verify the validity of the move
        if not is_move_valid(orig_dda, prevx, prevy, x, y):
            return (ret, False)

        if x == x1 and y == y1:
            return(ret, True)
        
        if m[y][x] == 1:
            return(ret, False)

        ret.append((x,y))
        prevx = x
        prevy = y
        i += 1

    return (ret, True)

# That part of code is used for reference path visualization
class line_type(Enum):
    FLOOR = 0
    ROUND = 1
    CEIL = 2

def normal_traceline(lt, source, target):
    x0, y0 = source
    x1, y1 = target

    dda = dda_data(x0, y0, x1, y1)
    ret = []
    i = 1
    
    if lt is line_type.FLOOR:
        fnc = dda.calc_floor_pos
    elif lt is line_type.ROUND:
        fnc = dda.calc_pos
    elif lt is line_type.CEIL:
        fnc = dda.calc_ceil_pos
    
    while(True):
        x, y = fnc(i)
        if x == x1 and y == y1:
            return (ret, True)
        ret.append((x,y))
        i += 1
