#!/usr/bin/env python3

import utils 
import os 
from shoot_tracer import trace_shoot
import math

def calc_dds(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    step = 0

    adx = abs( dx )
    ady = abs( dy )

    step = adx if adx >= ady else ady
    
    dx = dx / step
    dy = dy / step

    return (dx, dy, int(step))

if __name__ == "__main__":
    x0, y0 = (0.0, 0.0)
    x1, y1 = (1.0, 5.0)

    bx0 = x0
    by0 = y0

    dx,dy,step = calc_dds(x0,y0,x1,y1)

    print("Step: {0}".format(step))
    print("dx: {0}, dy: {1}".format(dx,dy))

    for i in range(0, step + 1):
        x0 = bx0 + i * dx
        y0 = by0 + i * dy
        
        print((round(x0),round(y0),i))
