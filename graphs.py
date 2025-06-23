class Graph:
    """Simple undirected weighted graph."""

    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.edges = {}

    def add_edge(self, u, v, w=1):
        if u > v:
            u, v = v, u
        self.edges[(u, v)] = w

    def weight(self, u, v):
        if u > v:
            u, v = v, u
        return self.edges.get((u, v), 0)

    def vertices(self):
        return range(self.num_vertices)

    def all_edges(self):
        for (u, v), w in self.edges.items():
            yield u, v, w
