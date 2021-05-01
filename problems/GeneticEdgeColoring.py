import random

import numpy as np

from problems.EdgeColoring import EdgeColoring


class GeneticEdgeColoring(EdgeColoring):

    def singlePointCrossover(self, parent1, parent2):
        matingIndex = random.randrange(len(parent1))
        childVec = np.concatenate((parent1[:matingIndex], parent2[matingIndex:]))
        return childVec

    def mutate(self, vec, numOfColors):

        for curVertex in range(len(vec)):
            neighbors = self.getNeighbors(curVertex)

            i = 0
            vertexChanged = True
            while i < len(neighbors) and vertexChanged:
                if vec[curVertex] == vec[neighbors[i]]:
                    vec[curVertex] = random.randint(0, numOfColors)
                    vertexChanged = False

        return vec
