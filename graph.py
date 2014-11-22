import uuid
import random

vertexCount = 0

class graph():
    def __init__(self):
        self.edges = dict()

    def addVertex(self, v):
        """ Vertex not already in graph will be added """
        if v in self.edges:
            print("ERROR: Vertex already exists in dictionary")
            return
        self.edges[v] = list()

    def addEdge(self, v1, v2):
        """ Directed edge created from v1 to v2 """
        assert v1 != v2
        if not v2 in self.edges[v1]:
            self.edges[v1].append(v2)

    def addUndirectedEdge(self, v1, v2):
        """ Adds reciprocal edges between vertices """
        self.addEdge(v1, v2)
        self.addEdge(v2, v1)

    def removeEdge(self, v1, v2):
        """ Removes v2 from v1 edge list """
        if v2 in self.edges[v1]:
            self.edges[v1].remove(v2)

    def removeUndirectedEdge(self, v1, v2):
        """ Removes reciprocal edges between vertices """
        self.removeEdge(v1, v2)
        self.removeEdge(v2, v1)

    def totallyConnect(self):
        """ Create an edge between every pair of vertices """
        for v1 in self.edges:
            for v2 in self.edges:
                if v1 != v2:
                    self.addEdge(v1, v2)

    def removeRandomUndirectedEdge(self):
        if not self.edges:
            print("ERROR: No edges to be removed")
            return
        v1 = None
        v2 = None
        while v2 == None:
            v1 = random.choice(list(self.edges.keys()))
            if self.edges[v1]:
                v2 = random.choice(self.edges[v1])
        self.removeUndirectedEdge(v1, v2)


class vertex():
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.id = self.getId()

    def getId(self):
        global vertexCount
        id = vertexCount
        vertexCount += 1
        return id

