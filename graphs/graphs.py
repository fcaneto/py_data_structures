from collections import namedtuple
"""
G = (E, V)
"""

Edge = namedtuple("Edge", ['to', 'weight'])

class Graph(object):

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices[v] = []

    def get_edges(self, v):
        if v in self.vertices:
            return self.vertices[v]
        else:
            return []

    def add_edge(self, v1, v2, directed=False, weight=None):
        edge = Edge(to=v2, weight=weight)

        self.add_vertex(v1)
        self.vertices[v1].append(edge)

        if not directed:
            self.add_edge(v2, v1, directed=True, weight=weight)

    @property
    def vertices_list(self):
        return self.vertices.keys()

    @property
    def num_vertices(self):
        return len(self.vertices.keys())

    @classmethod
    def from_tuple_list(cls, edge_list, directed=False):
        g = Graph()

        for e in edge_list:
            g.add_edge(e[0], e[1], directed)

        return g

    def __repr__(self):
        txt = []
        for v in self.vertices:
            for e in self.vertices[v]:
                txt.append('(%s, %s), ' % (v, e.to)) 

        return ''.join(txt)


