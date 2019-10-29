import pprint
from line_tracer import trace_line
from line_tracer import calc_dda

def sign( x ):
    if x == 0:
        return 0
    return 1 if x > 0 else -1

def refine_src_position(m,source,destination):
    x0, y0 = source
    x1, y1 = destination 

    # use same algorithm as for line tracing
    dx, dy, _ = calc_dda(x0, y0, x1, y1)
   
    # perform one step of the algorithm
    x = round(x0 + dx)
    y = round(y0 + dy)

    # detect if we moved in x or y or both
    inc_x = abs(x - x0) == 1
    inc_y = abs(y - y0) == 1

    # calculate direction for x and y
    sx = sign(x1 - x0)
    sy = sign(y1 - y0)

    if m[y][x]: # if there is cover we try to find out if it does block path
        # if we did move only one direction let's try to compensate for that
        if not inc_x: # position refinment for cover
            x += sx
        if not inc_y: # position refinment for cover
            y += sy 

        if inc_x and inc_y: # we've moved diagonally and there is a cover, let's check other options
            if abs(dx) == abs(dy): # ideally diagonal - no hit chance
                return ((x,y),False)

            if abs(dx) < abs(dy) and not m[y][x - sx]: # check if target is below or above the diagonal line
                x -= sx
            elif abs(dy) < abs(dx) and not m[y - sy][x]:
                y -= sy 

    if m[y][x]: # still obstacle so no route to target
        return ((x,y),False)

    return ((x,y),True)

def trace_shot(m,source,destination):
    # calculate refined positions for taking cover into account
    refined_src,src_ref_res = refine_src_position(m,source,destination)
    refined_dst,dst_ref_res = refine_src_position(m,destination,source)
    
    x0,y0 = refined_src 
    x1,y1 = refined_dst 
    
    # check if refined positions are correct
    if not src_ref_res or not dst_ref_res:
        return ([], False)
    
    # use trace line algorithm to create path
    return trace_line(m, x0, y0, x1, y1)
