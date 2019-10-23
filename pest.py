#!/usr/bin/env python3

import utils 
import os 
from shoot_tracer import trace_shoot
import math

if __name__ == "__main__":
    x0, y0 = (0.0, 0.0)
    x1, y1 = (10.0, 3.0)

    bx0 = x0
    by0 = y0

    dx = x1 - x0
    dy = y1 - y0

    step = 0.0

    if math.fabs(dx) >= math.fabs(dy):
        step = math.fabs(dx)
    else:
        step = math.fabs(dy)

    dx = dx / step  
    dy = dy / step

    i = 0

    print("Step: {0}".format(step))
    print("dx: {0}, dy: {1}".format(dx,dy))

    while( True ):
        x0 = bx0 + i * dx
        y0 = by0 + i * dy
        
        print((round(x0),round(y0),i))
        
        if round(x0) == x1 and round(y0) == y1:
            print("+")
            break

        i += 1

        if i > step:
            break





        
