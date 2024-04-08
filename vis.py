from vec2d import Point as P
from vec2d import Vec2D as V
from convexpolygon import ConvexPolygon as cnvx_ngon

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as vis_ngon
import seaborn as sns

####################################################################################################################
sns.set_style("white", {'xtick.direction': u'in','ytick.direction': u'in'})
sns.set_context("poster")
####################################################################################################################

def create_vis_polygon ( pgon ):

    vts = []        
    for pt in pgon.verts:
        vts.append([pt.x, pt.y])
    
    return vis_ngon(np.array(vts), color=np.random.rand(3), alpha=0.6)
    
def vis_polygons ( pgons ):

    fig,ax = plt.subplots()

    for igon in pgons:

        p = create_vis_polygon(igon)  
        ax.add_patch(p)
        
    ax.autoscale()
    ax.set_aspect('equal')
    plt.show()

    return
        
if __name__=='__main__':

    # You may comment out the lines below
    # Note that cnvx_ngon is an alias for ConvexPolygon
    # See import statements in lines 1 - 9
    
    a = cnvx_ngon([P(1,0), P(0,1), P(-1,0), P(0,-1)])
    b = cnvx_ngon([P(3,0), P(-1,2), P(-1,0)])  
    c = cnvx_ngon([P(7,0), P(13,0), P(7,6)])
    
    vis_polygons([a, b, c])
