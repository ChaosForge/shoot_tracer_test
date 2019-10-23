#!/usr/bin/env python3

import utils 
import os 
from shoot_tracer import trace_shoot
import math
import pprint

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

def plot_line(x0, y0, x1, y1):
    ret = []

    dx, dy, step = calc_dds(x0, y0, x1, y1)

    for i in range(0, step + 1):
        x = x0 + i * dx
        y = y0 + i * dy
        ret.append((round(x), round(y)))

    return ret

if __name__ == "__main__":
    print(plot_line(0.0, 0.0, 1.0, 5.0))
    print(plot_line(1.0, 5.0, 0.0, 0.0))
    print(plot_line(0.0, 0.0, 1.0, 6.0))
    print(plot_line(1.0, 6.0, 0.0, 0.0))
