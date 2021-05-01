import numpy as np

from algorithms.Algorithm import Algorithm


class Backtracking(Algorithm):

    def findSolution(self, maxIter):
        vertices = self._problem.getVertices()
        numOfVertices = len(vertices)
        conflictSet = {vertex: [] for vertex in vertices}

        # num of coloring
        domain = 2
        solution = {}

        while domain <= numOfVertices:
            verticesDomains = {vertex: list(range(domain)) for vertex in vertices}
            self._recursiveBackJumping(vertices.copy(), solution, conflictSet, verticesDomains)
            if len(solution) == len(vertices):
                print(f'found sol with {domain} colors')
                return solution
            print(f'Didnt find sol with {domain} colors')
            domain += 1

        print('failed')
        return None


    def _recursiveBackJumping(self, unassignedVertices, solution, conflictSet, verticesDomains):

        if len(unassignedVertices) == 0:
            return True

        vertexToBeAssigned = self._problem.getMostConstraintVariable(unassignedVertices, solution)

        newValue = self._problem.getLeastConstrainingValue(vertexToBeAssigned, solution, verticesDomains)
        if newValue is not None:
            solution[vertexToBeAssigned] = newValue
            unassignedVertices.remove(vertexToBeAssigned)

            # update conflict set of neighbors
            neighbors = self._problem.getNeighbors(vertexToBeAssigned)
            for nei in neighbors:
                if nei not in solution.keys() and vertexToBeAssigned not in conflictSet[nei]:
                    conflictSet[nei].append(vertexToBeAssigned)

            foundSolution = self._recursiveBackJumping(unassignedVertices.copy(), solution, conflictSet,
                                                       verticesDomains)
            if foundSolution is True:
                return True
            else:
                unassignedVertices.insert(0, vertexToBeAssigned)
                solution.pop(vertexToBeAssigned)
                # if we didn't reached the first node from the dead-end's conflict set
                if foundSolution is not vertexToBeAssigned:
                    return foundSolution

        if len(conflictSet[vertexToBeAssigned]) > 0:
            vertexToJumpTo = next(iter(conflictSet[vertexToBeAssigned]))
            # update conflict set
            union = conflictSet[vertexToJumpTo] + conflictSet[vertexToBeAssigned]
            union.remove(vertexToJumpTo)
            conflictSet[vertexToJumpTo] = list(dict.fromkeys(union))

            return vertexToJumpTo

        return False
