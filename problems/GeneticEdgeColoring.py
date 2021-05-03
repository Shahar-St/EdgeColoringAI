import random

import numpy as np

from problems.EdgeColoring import EdgeColoring


class GeneticEdgeColoring(EdgeColoring):

    def crossover(self, parent1, parent2):
        matingIndex = random.randrange(self._numOfVertices)
        childVec = np.concatenate((parent1[:matingIndex], parent2[matingIndex:]))
        return np.array(childVec)

    def mutate(self, vec, numOfColors):
        for curVertex in range(len(vec)):
            neighbors = self.getNeighbors(curVertex)
            i = 0
            vertexChanged = False
            while i < len(neighbors) and not vertexChanged:
                if vec[curVertex] == vec[neighbors[i]]:
                    vec[curVertex] = np.random.randint(numOfColors)
                    vertexChanged = True
                i += 1

        return np.array(vec)
