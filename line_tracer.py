import math

def calc_dda(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    step = 0

    adx = abs( dx )
    ady = abs( dy )

    step = adx if adx >= ady else ady
    
    if step == 0:
        return (0, 0, step)

    dx = dx / step
    dy = dy / step

    return (dx, dy, step)

def trace_line(m, x0, y0, x1, y1):
    ret = []

    dx, dy, step = calc_dda(x0, y0, x1, y1)

    for i in range(0, step + 1):
        x = round(x0 + i * dx)
        y = round(y0 + i * dy)

        if m[y][x]:
            return (ret, False)

        ret.append((x,y))

    return (ret, True)
