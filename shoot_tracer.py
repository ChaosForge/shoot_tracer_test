import pprint

def sign( x ):
    if x == 0:
        return 0
    return 1 if x > 0 else -1

def trace_shoot(m,source,destination):
    route = []

    x0,y0 = source
    x1,y1 = destination

    sx = sign(x1 - x0)
    sy = sign(y1 - y0)
    dy = -abs(y1 - y0)
    dx = abs(x1 - x0)

    err = dx + dy

    # first iteration takes into an account map so we are trying to avoid the cover 
    e2 = 2 * err 
    
    inc_x = False
    inc_y = False

    if e2 >= dy:
        x0 += sx
        err += dy
        inc_x = True 

    if e2 <= dx:
        y0 += sy 
        err += dx
        inc_y = True

    if m[y0][x0]: # if there is a wall we try to find next free spot
        if not inc_x:
            x0 += sx 
        if not inc_y:
            y0 += sy 

        if inc_x and inc_y:
            e2 = 2 * err
            if abs(dx) == abs(dy): # ideally diagonal - no hit chance
                return (route,False)
            if e2 <= dx and not m[y0][x0 - sx]:
                x0 -= sx
            elif e2 >= dy and not m[y0 - sy][x0]:
                y0 -= sy 

        # recalculate dy and dx
        dy = -abs(y1 - y0)
        dx = abs(x1 - x0)
        err = dx + dy
    
    if m[y0][x0]: # still no route to target
        route.append((x0,y0))
        return (route,False)
    route.append((x0,y0))

    while(True):
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx: 
            err += dx
            y0 += sy
        if x0 == x1 and y0 == y1:
            break
        if x0 <= 0 or y0 <= 0 or x0 >= 16 or y0 >= 16:
            print("Out of bounds!")
            return (route, False)
        if m[y0][x0] == 1:
            return (route, False)
        route.append((x0,y0))

    return (route, True)
