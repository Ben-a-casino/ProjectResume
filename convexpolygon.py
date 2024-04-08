
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:22:15 2024

@author: benac
"""

from vec2d import Point
from vec2d import Vec2D

import math


def orient2d(a, b, c):

    '''

    Note that you will need this function only if you plan
    to code up the optional question listed in section 2.4.2
    
    Parameters
    ----------
        a : Point object
        b : Point object
        c : Point object
        
    Returns
    --------
        Integer 1/1/0
        Returns 1 if points are oriented in the 
        counter clockwise direction -1 if clockwise
        and 0 if collinear
        
    '''

    # Signed area of triangle formed by a,b,c
    s_a = (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)
    
    # Orientation
    result = 1 if s_a > 0 else -1 if s_a < 0 else 0
    
    return result



class ConvexPolygon:
    """
    This class rerpesents a convex polygon defined by a list of vertex points
    that allows for representation and maniuplation of a convex polygon through
    translation, rotation and scaling  of its vertices to change it's geometric 
    properties
    Attributes
    ----------
    verts : list of Point
        The vertices of the polygon.
    nverts : int
        The number of vertices in the polygon.
    edges : list of Vec2D
        The vector representations of the polygon's edges.
    Methods
    -------
    translate(vec)
        Translates the polygon by a given vector.
    rotate(angle, pivot=None)
        Rotates the polygon around a pivot point by a specified angle.
    scale(sx, sy, pivot=None)
        Scales the polygon relative to a pivot point by specified factors along the x and y axes.
    get_centroid()
        Computes and returns the centroid of the polygon.
    """
    def __init__(self, points):
        self.verts = points
        self.nverts = len(points)
        self.edges = [Vec2D(points[(i+1) % self.nverts].x - points[i].x, points[(i+1) % self.nverts].y - points[i].y) for i in range(self.nverts)]
        """
        Initialize a new ConvexPolygon instance.

        Parameters
        ----------
        points : list of Point
            The vertices of the polygon.
        
        Returns
        -------
        None.
        """
    def __str__(self):
        verts_str = ", ".join([str(v) for v in self.verts])
        edges_str = ", ".join([str(e) for e in self.edges])
        return 
        """
        Return a string representation of the ConvexPolygon instance.
        Returns
        -------
        str : The string representation of the polygon.
        """
    # Example method: Translate
    def translate(self, vec):
        self.verts = [Point(v.x + vec.x, v.y + vec.y) for v in self.verts]
        # Note: Edges do not change in length or direction, so no need to update them.
        """
        Translate the polygon by a given vector.
        Parameters
        ----------
        vec : Vec2D
            The vector by which to translate the polygon's vertices.
        Returns
        -------
        None.
        """
    def rotate(self, angle, pivot=None):
        if pivot is None:
            pivot = self.get_centroid()
    
        cos_theta, sin_theta = math.cos(angle), math.sin(angle)
        new_verts = []
    
        for vert in self.verts:
            dx = vert.x - pivot.x
            dy = vert.y - pivot.y
            new_x = dx * cos_theta - dy * sin_theta + pivot.x
            new_y = dx * sin_theta + dy * cos_theta + pivot.y
            new_verts.append(Point(new_x, new_y))
    
        self.verts = new_verts
        # Correctly recalculating edges
        self.edges = [Vec2D(self.verts[i], self.verts[(i + 1) % self.nverts]) for i in range(self.nverts)]
        """
        Rotate the polygon around a given pivot point by a specified angle.
        Parameters
        ----------
        angle : float
            The angle in radians by which to rotate the polygon.
        pivot : Point, optional
            The pivot point around which to rotate. Defaults to the centroid.
        Returns
        -------
        None.
        """
    def scale(self, sx, sy):
        centroid = self.get_centroid()
        new_verts = []
    
        for vert in self.verts:
            dx = (vert.x - centroid.x) * sx
            dy = (vert.y - centroid.y) * sy
            new_verts.append(Point(dx + centroid.x, dy + centroid.y))
    
        self.verts = new_verts
        self.edges = [Vec2D(self.verts[i], self.verts[(i + 1) % self.nverts]) for i in range(self.nverts)]
        """
        Scale the polygon relative to a pivot point by specified factors along the x and y axes.
        Parameters
        ----------
        sx : float
            The scaling factor along the x-axis.
        sy : float
            The scaling factor along the y-axis.
        pivot : Point, optional
            The pivot point for scaling. Defaults to the centroid.
        Returns
        -------
        None.
        """

    def translate(self, vector):
        """Translates the polygon by the given vector."""
        self.verts = [Point(v.x + vector.x, v.y + vector.y) for v in self.verts]

    def get_centroid(self):
        """Computes and returns the centroid of the polygon."""
        cx = sum(v.x for v in self.verts) / self.nverts
        cy = sum(v.y for v in self.verts) / self.nverts
        return Point(cx, cy)
        """
        Computes and returns the centroid of the polygon.
        Returns
        -------
        Point : The centroid of the polygon.
        """


    '''
    def __str__(self):

        nv = 'No. of Vertices: '+str(self.nverts)+'\n'
        vs = "Vertices "+" ".join([v.__str__() + ', ' for v in self.verts]) + '\n'
        es = "Edges "+ " ".join([e.__str__() + ', ' for e in self.edges]) 
        return nv + vs + es

    '''


    '''

    # Uncomment these lines if you'd like to run game.py
    
    @staticmethod
    def get_projections_minmax (ortho, obj_1, obj_2):

        # Edit from this line
        projections_obj_1 = [ortho * vert for vert in obj_1.verts]
        projections_obj_2 = [ortho * vert for vert in obj_2.verts]
        
        min_obj_1, max_obj_1 = min(projections_obj_1), max(projections_obj_1)
        min_obj_2, max_obj_2 = min(projections_obj_2), max(projections_obj_2)
        
        return min_obj_1, max_obj_1, min_obj_2, max_obj_2 
        
    

    def __and__(self, other):
        
        #Uses separating axes theorem to check for overlaps

        all_edges = self.edges + other.edges
        
        for edge in all_edges:

            ortho = edge.normal_ccw()
            
            min_self, max_self, min_other, max_other = self.get_projections_minmax(ortho, self, other) 
            
            # Check for overlaps in projection
            if min_self > max_other or max_self < min_other:
                
                # Gap found in projections and therefore Overlap cannot occur
                return False
            
        return True
    

    '''

    
    
   
if __name__=='__main__':
    
    pass