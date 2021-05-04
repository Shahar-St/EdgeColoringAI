import copy

import numpy as np

from algorithms.Algorithm import Algorithm


class BackJumping(Algorithm):

    def findSolution(self, maxIter):
        vertices = self._problem.getVertices()
        conflictSet = {vertex: [] for vertex in vertices}

        # num of coloring
        domain = self._problem.getLowerBound()
        solution = {}
        upperBound = self._problem.getUpperBound()

        while domain <= upperBound:
            verticesDomains = {vertex: list(range(domain)) for vertex in vertices}
            self._recursiveBackJumping(vertices.copy(), solution, copy.deepcopy(conflictSet),
                                       copy.deepcopy(verticesDomains))
            if len(solution) == len(vertices):
                resVec = np.empty((self._problem.getNumOfVertices()), dtype=int)
                for vertex, color in solution.items():
                    resVec[vertex] = color

                numOfSearchedStates = self._numOfSearchedStates
                self._numOfSearchedStates = 0
                return resVec, numOfSearchedStates

            print(f'Didnt find solution with {domain} colors')
            domain += 1

        numOfSearchedStates = self._numOfSearchedStates
        self._numOfSearchedStates = 0
        return None, numOfSearchedStates

    def _recursiveBackJumping(self, unassignedVertices, solution, conflictSet, verticesDomains):

        if len(unassignedVertices) == 0:
            return -1, -1

        vertexToBeAssigned = self._problem.getMostConstraintVariable(unassignedVertices, solution)
        # build conflict set of neighbors (we do that here to keep the ordering
        neighbors = self._problem.getNeighbors(vertexToBeAssigned)
        for nei in neighbors:
            if nei not in solution.keys() and vertexToBeAssigned not in conflictSet[nei]:
                conflictSet[nei].append(vertexToBeAssigned)

        foundValue = True
        while len(verticesDomains[vertexToBeAssigned]) > 0 and foundValue:
            newValue = self._problem.getLeastConstrainingValue(vertexToBeAssigned, solution, verticesDomains)
            if newValue is None:
                foundValue = False
            else:
                self._numOfSearchedStates += 1

                solution[vertexToBeAssigned] = newValue
                unassignedVertices.remove(vertexToBeAssigned)

                # update conflict set vertices domains
                for neighbor in conflictSet[vertexToBeAssigned]:
                    if newValue in verticesDomains[neighbor]:
                        verticesDomains[neighbor].remove(newValue)

                res = self._recursiveBackJumping(unassignedVertices, solution, conflictSet, verticesDomains)
                # success (-1) or need to jump higher
                if res[0] != vertexToBeAssigned:
                    return res

                # conflict in child:
                # remove assignment, remove value from domain
                solution.pop(vertexToBeAssigned)
                verticesDomains[vertexToBeAssigned].remove(newValue)
                unassignedVertices.append(vertexToBeAssigned)
                # return value to vertices in CS
                for vertex in conflictSet[vertexToBeAssigned]:
                    if newValue not in verticesDomains[vertex] \
                            and not self._hasConflictsWithValue(vertex, newValue, conflictSet, solution):
                        verticesDomains[vertex].append(newValue)

                # update conflict set
                union = conflictSet[res[1]] + conflictSet[vertexToBeAssigned]
                union.remove(vertexToBeAssigned)
                conflictSet[vertexToBeAssigned] = list(dict.fromkeys(union))

        if len(conflictSet[vertexToBeAssigned]) > 0:
            vertexToJumpTo = conflictSet[vertexToBeAssigned][0]
            return vertexToJumpTo, vertexToBeAssigned

        return -1, -1

    def _hasConflictsWithValue(self, vertex, value, conflictSet, solution):
        for ver in conflictSet[vertex]:
            if ver in solution and solution[ver] == value:
                return True
        return False
