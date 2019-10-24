# Shoot Tracer Test

Test of shoot tracing algorithm for JupiterHell.

# Problem

Current implementation uses Bresenham line rendering for tracincg shoots. The biggest issue with this approach is that it is not symmetrical. So taking into consideration two points on the map A and B tracing line from A to B may walk through different cells than tracing from B to A. In addition to that we have the cover system which requires some trickery when Bresenham algorithm is used. 

# Solution

During the research we've found that we need numerically stable solution in order to be able to find exact same path regardless the order of start and end point. We've found that modified dda approach gives the best result. In order to solve the cover system we simply sample the line once and we refine the starting position of the line taking into an account possible covers. 

# Results
