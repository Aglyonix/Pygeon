"""
# The Algorithm of Bowyer Watson
#### step 1 : Declaring the supra triangle
#### step 2 : for each point remove the bad triangle and do the triangulation
"""

import numpy as np

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(s):
        return "( " + str(s.x) + ", " + str(s.y) + " )"

    def __add__(self, b):
        return Point(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Point(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Point(b * self.x, b * self.y)

    __rmul__ = __mul__

    def IsInCircumcircleOf(self, T):
        """
        Find if the point is in the circumcircle T
        """

        a_x = T.v[0].x
        a_y = T.v[0].y

        b_x = T.v[1].x
        b_y = T.v[1].y

        c_x = T.v[2].x
        c_y = T.v[2].y

        # The point coordinates

        d_x = self.x
        d_y = self.y

        # If the following determinant is greater than zero then point lies inside circumcircle
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])

        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False
        
class Triangle:

    def __init__(self, a, b, c):
        self.v = [a, b, c]

        self.edges = [[self.v[0], self.v[1]],
                      [self.v[1], self.v[2]],
                      [self.v[2], self.v[0]]]

        self.neighbour = [None] * 3

    def HasVertex(self, point):
        if (self.v[0] == point) or (self.v[1] == point) or (self.v[2] == point):
            return True
        return False

    def __repr__(s):
        return str(s.v)
    
class Delaunay_Triangulation:
    def __init__(self, w, h):
        self.triangulation = []

        # Declaring the supra triangle coordinate information
        self.SupraPointA = Point(-100, -100)
        self.SupraPointB = Point(2 * w + 100, - h // 2)
        self.SupraPointC = Point(- w // 2, 2 * h + 100)

        supraTriangle = Triangle(self.SupraPointA, self.SupraPointB, self.SupraPointC)

        self.triangulation.append(supraTriangle)

    def AddPoint(self, p):

        bad_triangles = []

        for triangle in self.triangulation:
            # Check if the given point is inside the circumcircle of triangle
            if p.IsInCircumcircleOf(triangle):
                # If it is then add the triangle to bad triangles
                bad_triangles.append(triangle)

        polygon = []

        # Routine is to find the convex hull of bad triangles
        # This involves a naive search method, which increases the time complexity
        for current_triangle in bad_triangles:
            for this_edge in current_triangle.edges:
                isNeighbour = False
                for other_triangle in bad_triangles:
                    if current_triangle == other_triangle:
                        continue
                    for that_edge in other_triangle.edges:
                        if (this_edge[0] == that_edge[0] and this_edge[1] == that_edge[1]) or (this_edge[0] == that_edge[1] and this_edge[1] == that_edge[0]):
                            # Check if the Edge is shared between two triangles
                            # If the edge is shared it won't be included into the convex hull
                            isNeighbour = True
                if not isNeighbour:
                    polygon.append(this_edge)

        # Delete the bad triangles
        for each_triangle in bad_triangles:
            self.triangulation.remove(each_triangle)

        # Re-triangle the convex hull using the given point
        for each_edge in polygon:
            newTriangle = Triangle(each_edge[0], each_edge[1], p)
            self.triangulation.append(newTriangle)

    def Remove_Supra_Triangles(self):
        # Removing the super triangle using Lamba function
        onSupra = lambda triangle: triangle.HasVertex(self.SupraPointA) or triangle.HasVertex(self.SupraPointB) or triangle.HasVertex(self.SupraPointC)

        for triangle_new in self.triangulation[:]:
            if onSupra(triangle_new):
                self.triangulation.remove(triangle_new)