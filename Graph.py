import numpy as np
from heapq import *
from random import *

class Vertex:
    def __init__(self, value, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.value = value
        self.adjacent_v = {}
        self.in_three = False
        self.parent = None

    def __repr__(s):
        return f"{s.value} (" + str(s.x) + ", " + str(s.y) + ")"

    def __add__(self, b):
        return Vertex(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Vertex(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Vertex(b * self.x, b * self.y)

    __rmul__ = __mul__

    def addedge(self, vertex, weight=0) -> None:
        self.adjacent_v[vertex] = Edge(self, vertex, weight)

    def IsInCircumcircleOf(self, T):
        """
        Find if the Vertex is in the circumcircle T
        """

        a_x = T.v[0].x
        a_y = T.v[0].y

        b_x = T.v[1].x
        b_y = T.v[1].y

        c_x = T.v[2].x
        c_y = T.v[2].y

        # The Vertex coordinates

        d_x = self.x
        d_y = self.y

        # If the following determinant is greater than zero then Vertex lies inside circumcircle
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])

        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False
        
class Edge:

    def __init__(self, vertex_a: Vertex, vertex_b: Vertex, weight=1, oriented=0) -> None:
        self.vertices = [vertex_a, vertex_b]
        self.weight = weight
        self.oriented = oriented # 0 if is not oriented, 1 if oriented toward vertex b and -1 toward a 

"""
# The Algorithm of Bowyer Watson
#### step 1 : Declaring the supra triangle
#### step 2 : for each Vertex remove the bad triangle and do the triangulation
"""

class Triangle:

    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self.v = [a, b, c]

        self.edges = [Edge(self.v[0], self.v[1]),
                      Edge(self.v[1], self.v[2]),
                      Edge(self.v[2], self.v[0])]

        self.neighbour = [None] * 3

    def HasVertex(self, Vertex):
        if (self.v[0] == Vertex) or (self.v[1] == Vertex) or (self.v[2] == Vertex):
            return True
        return False

    def __repr__(s):
        return str(s.v)
    
class Delaunay_Triangulation:

    def __init__(self, w, h):
        self.triangulation = []

        # Declaring the supra triangle coordinate information
        self.SupraVertexA = Vertex(-100, -100)
        self.SupraVertexB = Vertex(2 * w + 100, - h // 2)
        self.SupraVertexC = Vertex(- w // 2, 2 * h + 100)

        supraTriangle = Triangle(self.SupraVertexA, self.SupraVertexB, self.SupraVertexC)

        self.triangulation.append(supraTriangle)

    def AddVertex(self, p):

        bad_triangles = []

        for triangle in self.triangulation:
            # Check if the given Vertex is inside the circumcircle of triangle
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
                        if (this_edge.vertices[0] == that_edge.vertices[0] and this_edge.vertices[1] == that_edge.vertices[1]) or (this_edge.vertices[0] == that_edge.vertices[1] and this_edge.vertices[1] == that_edge.vertices[0]):
                            # Check if the Edge is shared between two triangles
                            # If the edge is shared it won't be included into the convex hull
                            isNeighbour = True
                if not isNeighbour:
                    polygon.append(this_edge)

        # Delete the bad triangles
        for each_triangle in bad_triangles:
            self.triangulation.remove(each_triangle)

        # Re-triangle the convex hull using the given Vertex
        for each_edge in polygon:
            newTriangle = Triangle(each_edge.vertices[0], each_edge.vertices[1], p)
            self.triangulation.append(newTriangle)

    def Remove_Supra_Triangles(self):
        # Removing the super triangle using Lamba function
        onSupra = lambda triangle: triangle.HasVertex(self.SupraVertexA) or triangle.HasVertex(self.SupraVertexB) or triangle.HasVertex(self.SupraVertexC)

        for triangle_new in self.triangulation[:]:
            if onSupra(triangle_new):
                self.triangulation.remove(triangle_new)

class Graph:

    def __init__(self) -> None:
        self.vertices = []
        self.edges = []
        self.new_edges = []

    def addvertex(self, vertex: Vertex) -> None:
        assert isinstance(vertex, Vertex)
        self.vertices.append(vertex)

    def addvertices(self, vertices: list[Vertex]) -> None:
        for vertex in vertices:
            assert isinstance(vertex, Vertex)
            self.vertices.append(vertex)

    def addedge(self, edge: Edge) -> None:
        assert isinstance(edge, Edge)
        self.edges.append(edge)

    def addedges(self, edges: list[Edge]) -> None:
        for edge in edges:
            assert isinstance(edge, Edge)
            self.edges.append(edges)

    def is_empty(self):
        if self.vertices == []:
            return True
        return False
    
    def triangulation(self) -> None:
        assert not self.is_empty(), 'You can not triangulate an empty graph'

        w = max([v.x for v in self.vertices])
        h = max([v.y for v in self.vertices])
        Algo = Delaunay_Triangulation(w, h)
        
        for v in self.vertices:
            Algo.AddVertex(v)
        Algo.Remove_Supra_Triangles()

        for triangle in Algo.triangulation:
            for edge in triangle.edges:
                if edge not in self.edges:
                    self.edges.append(edge)

    def prims_algorithm(self) -> None:
        distance = {}
        remaining = heapify([])
        weight = 0
        start_vertex = choice(self.vertices)

        for vertex in self.vertices:
            distance[vertex] = remaining[vertex] = float('inf')


        distance[start_vertex] = remaining[start_vertex] = 0

        while len(remaining) > 0:
            v = remaining.popitem([0])
            v.in_three = True
            if v != start_vertex:
                weight += distance[v]

            for edge in v.edges:
                w = edge.vertex
                if distance[w] > edge.weight and w.in_three == False:
                    distance[w] = remaining[w] = edge.weight
                    w.parent = v

        for v in self.vertices:
            if v != start_vertex:
                print(f"{v.parent.value} - {v.value}")

        return weight