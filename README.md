# Shoot Tracer Test

Test of shoot tracing algorithm for JupiterHell.

# Problem

Current implementation uses Bresenham line rendering for tracincg shoots. The biggest issue with this approach is that it is not symmetrical. So taking into consideration two points on the map A and B tracing line from A to B may walk through different cells than tracing from B to A. In addition to that we have the cover system which requires some trickery when Bresenham algorithm is uses. 

# Solution


