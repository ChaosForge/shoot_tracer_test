import math
from enum import Enum

class dda_dir(Enum):
    DDA_NONE = 0
    DDA_X  = 1
    DDA_Y  = 2
    DDA_XY = 3

class dda_data(object):
    __slots__ = ['x0', 'y0', 'dx', 'dy', 'odx', 'ody', 'step', 'd_dir']
    def __init__(self, src, dst):
        x0, y0 = src
        x1, y1 = dst

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
        print("Big skip!")
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

def calc_pos(m, dda, i, possible_moves):
    x_f, y_f = dda.calc_floor_pos(i)
    x_r, y_r = dda.calc_pos(i)
    x_c, y_c = dda.calc_ceil_pos(i)

    r_valid = m[y_r][x_r] != 1
    c_valid = m[y_c][x_c] != 1
    f_valid = m[y_f][x_f] != 1

    if r_valid and (x_r, y_r) in possible_moves:
        x, y = x_r, y_r
    elif f_valid and (x_f, y_f) in possible_moves:
        x, y = x_f, y_f
    elif c_valid and (x_c, y_c) in possible_moves:
        x, y = x_c, y_c
    else:
        return ((0, 0), False)

    return ((x, y), True)

def calc_possible_moves(m, dda, i):
    ret = set()

    x_f, y_f = dda.calc_floor_pos(i)
    x_r, y_r = dda.calc_pos(i)
    x_c, y_c = dda.calc_ceil_pos(i)

    r_valid = m[y_r][x_r] != 1
    c_valid = m[y_c][x_c] != 1
    f_valid = m[y_f][x_f] != 1

    if f_valid:
        ret.add((x_f, y_f))

    if c_valid:
        ret.add((x_c, y_c))

    if r_valid:
        ret.add((x_r, y_r))

    return ret 

def trace_line(m, src, dst, ref_src, ref_dst):
    ret = []
    
    ref_dda = dda_data(ref_src, ref_dst)
    dda = dda_data(src, dst)

    i = 1
    j = 2
    
    prevx = ref_src[0]
    prevy = ref_src[1]
    
    ret.append((prevx, prevy))
    
    while( True ):

        # See how it works with refinment of starting positions as fixed tiles for targetting
        # Calculate two dda's one for original direction, second one for refinment positions
        # At each step check if the refinment one matches one of the original ones, should work
        pos_moves = calc_possible_moves(m, dda, j)
        new_ref_pos, res = calc_pos(m, ref_dda, i, pos_moves)
        
        if not res:
            return (ret, False)

        x, y = new_ref_pos

        # Verify the validity of the move
        if i > 0 and not is_move_valid(ref_dda, prevx, prevy, x, y):
            return (ret, False)

        if x == ref_dst[0] and y == ref_dst[1]:
            ret.append((x,y))
            return(ret, True)
        
        if m[y][x] == 1:
            return(ret, False)

        ret.append((x,y))
        prevx = x
        prevy = y
        i += 1
        j += 1

    return (ret, True)

# That part of code is used for reference path visualization
class line_type(Enum):
    FLOOR = 0
    ROUND = 1
    CEIL = 2

def normal_traceline(lt, source, target):
    dda = dda_data(source, target)
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
        if x == target[0] and y == target[1]:
            return (ret, True)
        ret.append((x,y))
        i += 1
