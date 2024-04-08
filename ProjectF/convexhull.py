
import math
from convexpolygon import ConvexPolygon 
from vec2d import Point as P
from vec2d import Vec2D
from vis import create_vis_polygon

def area2 (a, b, c):
    '''
    
    Parameters
    ----------
    a : Point object
        Vertex of a triangle.
    b : Point object
        ertex of a triangle.
    c : Point object
        Vertex of a triangle.

    Returns
    -------
    Int/Float
        Signed area of triangle formed by points a,b,c.

    '''
    # Compute signed area
    return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)
    

def is_ccw(a, b, c):
    '''

    Parameters
    ----------
    a : Point object
    b : Point object
    c : Point object

    Returns
    -------
    Boolean
        Returns True if points are oriented in the 
        counter clockwise direction

    '''

    return area2(a,b,c) > 0

def get_leftmost_point(points):
    leftmost = points[0]
    for point in points[1:]:
        if point.x < leftmost.x or (point.x == leftmost.x and point.y < leftmost.y):
            leftmost = point
    return leftmost
    """
    This finds the leftmost point from a list of points, if two points have the same
    x-coordinate, the one with the lower y coordinate is considered the leftmost
    Parameters:
        points (list of Point): The list of Point instances to search.
    Returns:
        Point: The leftmost point in the list.
    """

def get_convex_hull ( points ):
    # Sort points lexicographically by x and y
    points = sorted(points, key=lambda p: (p.x, p.y))

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and not is_ccw(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and not is_ccw(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hulls; remove duplicates
    convex_hull = lower[:-1] + upper[:-1]
    return ConvexPolygon(convex_hull)
    pass
    """
    This computes the convex hull of aa set of points using Graham scaan algorithm. The convex
    hull is the smallest convex polygon that has all the points in the set,.
    Parameters:
        points (list of Point): The list of points from which to construct the convex hull.
    Returns:
        ConvexPolygon: The convex hull of the points as a ConvexPolygon instance.
    """
       
def plot_convex_hull ( points, chull, filename = None ):
    '''  

    Parameters
    ----------
    points : List
        a List of Point objects.
    chull : ConvexPolygon
        ConvexPolygon object that is a convex hull.
    filename : string, optional
        DFilename for saving the plot.

    Returns
    -------
    None.

    '''

    import matplotlib.pyplot as plt
    import seaborn as sns

    # Create plot object
    fig, ax = plt.subplots()

    # Get x coordinates and y coordinates
    xps = [p.x for p in points]
    yps = [p.y for p in points]

    # Get x,y coordinates of polygon vertices
    poly_x = [p.x for p in chull.verts]
    poly_y = [p.y for p in chull.verts]

    # Closing the polygon
    poly_x.append(chull.verts[0].x)
    poly_y.append(chull.verts[0].y)
    
    # Scatter plot of points
    ax.scatter(xps, yps, c = '#000000', s = 15)

    # Plot convex hull
    ax.plot(poly_x, poly_y, linewidth = 3)
    p = create_vis_polygon(chull)  
    ax.add_patch(p)

    # left most point
    ax.scatter(poly_x[0], poly_y[0], c = 'r', s = 25)
    
    ax.set_xlabel('x', fontsize=20)
    ax.set_ylabel('y', fontsize=20)
    
    plt.tight_layout()

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

    
if __name__=='__main__':
    
    pts  = [P(2,4), P(1,2), P(2,5), P(4,5), P(2,6)]
    
    #plot_convex_hull(pts, get_convex_hull(pts))
    #print(get_leftmost_point([P(-1,0), P(-1,3), P(-1,5), P(-1,7)]))
