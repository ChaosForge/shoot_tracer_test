# Shot Tracer Test

Test of shot tracing algorithm for JupiterHell.

# Problem

Current implementation uses Bresenham line rendering for tracincg shoots. The biggest issue with this approach is that it is not symmetrical. So taking into consideration two points on the map A and B tracing line from A to B may walk through different cells than tracing from B to A. In addition to that we have the cover system which requires some trickery when Bresenham algorithm is used. 

# Solution

During the research we've found that we need numerically stable solution in order to be able to find exact same path regardless the order of start and end point. We've found that modified DDA approach gives the best result. In order to solve the cover system we simply sample the line once and we refine the starting position of the line taking into an account possible covers. 

# Prerequisites

In order to run tests Python 3.x is needed plus NumPy and pypng libraries

# Usage

Test cases are stored within the /cases dir. Each file is a separate map with walls marked using '#', Player '@' and enemy is marked by 'h'. First line is an expected test result. 

# Test description

During the test our approach is used twice. First algorithm tries to find route from the player to the enemy then from the enemy to the player. Test framework compares results with the expected result and prints out the test outcome. In addition the \*.png picture is rendered with the presentation of route found via the algorithm. Test framework uses alpha blending in order to determine the color of each cell so if the line tracing algorithm wouldn't be symmetrical it would render route cells using two different colors.

# Known issues

At this point test framework does not verifies symmetricity of paths autmatically.
