import copy
from queue import Queue

import numpy as np

from algorithms.Algorithm import Algorithm


class ForwardChecking(Algorithm):

    def findSolution(self, maxIter):
        vertices = self._problem.getVertices()
        domain = self._problem.getLowerBound()
        solution = {}
        upperBound = self._problem.getUpperBound()

        while domain <= upperBound:
            verticesDomains = {vertex: list(range(domain)) for vertex in vertices}
            self._recursiveForwardChecking(vertices.copy(), solution, copy.deepcopy(verticesDomains))
            if len(solution) == len(vertices):
                resVec = np.empty((self._problem.getNumOfVertices()), dtype=int)
                for vertex, color in solution.items():
                    resVec[vertex] = color
                return resVec

            print(f'Didnt find solution with {domain} colors')
            domain += 1

        return None

    def _recursiveForwardChecking(self, unassignedVertices, solution, verticesDomains):
        if len(unassignedVertices) == 0:
            return True

        # get variable and value
        vertexToBeAssigned = self._problem.getMostConstraintVariable(unassignedVertices, solution)
        newValue = self._problem.getLeastConstrainingValue(vertexToBeAssigned, solution, verticesDomains)
        if newValue is None:
            return False

        # set the value to the variable
        solution[vertexToBeAssigned] = newValue
        unassignedVertices.remove(vertexToBeAssigned)
        verticesDomains[vertexToBeAssigned] = [newValue]

        # remove value from v's neighbors
        neighbors = self._problem.getNeighbors(vertexToBeAssigned)
        for nei in neighbors:
            if newValue in verticesDomains[nei]:
                verticesDomains[nei].remove(newValue)

        # maintain arc consistency
        self.ac3(verticesDomains)
        for unassignedVertex in unassignedVertices:
            if len(verticesDomains[unassignedVertex]) == 0:
                return False

        return self._recursiveForwardChecking(unassignedVertices, solution, verticesDomains)

    def ac3(self, domains):
        arcsQueue = Queue()
        arcs = self._problem.getEdges()
        for arc in arcs:
            arcsQueue.put(arc)

        while not arcsQueue.empty():
            arc = arcsQueue.get()
            if self.removeInconsistentValues(arc, domains):
                for neighbor in self._problem.getNeighbors(arc[0]):
                    arcsQueue.put((arc[0], neighbor))

    def removeInconsistentValues(self, arc, domains):
        v1 = arc[0]
        v2 = arc[1]

        uniqueValuesOfV2 = set(domains[v2])
        if len(uniqueValuesOfV2) == 0:
            return False

        if len(uniqueValuesOfV2) > 1:
            return False

        valueInV2 = uniqueValuesOfV2.pop()
        if valueInV2 in domains[v1]:
            domains[v1].remove(valueInV2)
            return True

        return False
