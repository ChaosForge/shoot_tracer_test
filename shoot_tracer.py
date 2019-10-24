import pprint
from line_tracer import trace_line 

def sign( x ):
    if x == 0:
        return 0
    return 1 if x > 0 else -1

def refine_src_position(m,source,destination):
    x0,y0 = source
    x1,y1 = destination 

    sx = sign(x1 - x0)
    sy = sign(y1 - y0)
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    
    err = dx + dy 
    e2 = 2 * err 

    inc_x = False
    inc_y = False
    
    # One step of bresenham to detect if there is a cover 
    if e2 >= dy:
        x0 += sx
        err += dy
        inc_x = True 

    if e2 <= dx:
        y0 += sy
        err += dx
        inc_y = True

    if m[y0][x0]: # if there is cover we try to find out if it does block path

        # if we did move only one direction let's try to compensate for that
        if not inc_x: # position refinment for cover
            x0 += sx
        if not inc_y: # position refinment for cover
            y0 += sy 

        if inc_x and inc_y: # we've moved diagonally and there is a cover, let's check other options
            if abs(dx) == abs(dy): # ideally diagonal - no hit chance
                return ((x0,y0),False)

            if abs(dx) < abs(dy) and not m[y0][x0 - sx]: # check if target is below or above the diagonal line
                x0 -= sx
            elif abs(dy) < abs(dx) and not m[y0 - sy][x0]:
                y0 -= sy 

    if m[y0][x0]: # still obstacle so no route to target
        return ((x0,y0),False)

    return ((x0,y0),True)

def trace_shoot(m,source,destination):
    route = []
    
    # calculate refined positions for taking cover into account
    refined_src,src_ref_res = refine_src_position(m,source,destination)
    refined_dst,dst_ref_res = refine_src_position(m,destination,source)
    
    x0,y0 = refined_src 
    x1,y1 = refined_dst 
    
    # check if refined positions are correct
    if not src_ref_res or not dst_ref_res:
        return (route, False)
    
    # use trace line algorithm to create path
    return trace_line(m, x0, y0, x1, y1)
