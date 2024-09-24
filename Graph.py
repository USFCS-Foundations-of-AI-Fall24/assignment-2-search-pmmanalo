## this time around our Nodes will contain strings.

class Node :
    ### here's how we do constructors.
    def __init__(self, val=""):
        self.value = val
    def __hash__(self):
        return hash(self.value)
    def __repr__(self):
        return str(self.value)
    def __eq__(self, other):
        return self.value == other.value

## now src and dest are going to be strings.
class Edge:
    def __init__(self, src, dest, val=0):
        self.src = src
        self.dest = dest
        self.val = val
    def __repr__(self):
        return "(%s %s %d)" % (self.src, self.dest, self.val)

class Graph :
    def __init__(self,n_vertices=5):
        ## our adjacency list
        self.g = {}

    def add_node(self, index):
            self.g[index] = []

    def add_edge(self, e):
        self.g[e.src].append(e)

    def get_edge(self, src, dest):
        if src in self.g :
            edges = self.g[src]
            for e in edges :
                if e.dest == dest :
                    return e
        
    def get_neighbors_and_costs(self, node):
        if node in self.g:
            return [(a.dest, a.val) for a in self.g[node]]
        return []