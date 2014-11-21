
import graph

class character(graph.vertex):
    """ Actor/agent within the story """
    def __init__(self):
        self.name = None
        self.victim = False

# Create graph
g = graph.graph()
# Add characters
totalCharacters = 5
for n in range(totalCharacters):
    g.addVertex(character())
# Totally connect graph
g.totallyConnect()
# Eliminate some random edges
numEliminatedEdges = 5
for n in range(numEliminatedEdges):
    g.removeRandomUndirectedEdge()

print(g.edges)