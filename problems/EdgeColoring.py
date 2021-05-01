import os
import random

import numpy as np


class EdgeColoring:

    def __init__(self, fileName):
        filePath = os.getcwd() + '\\util\\instances\\' + fileName
        inputFile = open(filePath, 'r')
        lines = [line[2:-1] for line in inputFile.readlines() if not line.startswith('c')]
        edgesAndVertices = lines[0].split(' ')[1:]
        numOfVertices = int(edgesAndVertices[0])
        numOfEdges = int(edgesAndVertices[1])
        graphMatrix = np.full((numOfEdges, numOfEdges), False)
        for edge in lines[1:]:
            vertices = edge.split(' ')
            graphMatrix[int(vertices[0]) - 1][int(vertices[1]) - 1] = True
            graphMatrix[int(vertices[1]) - 1][int(vertices[0]) - 1] = True

        print('Input File:' + fileName)
        print(f'# of edges: {numOfEdges}, # of vertices: {numOfVertices}')
        print(f'Graph density: {((2 * numOfEdges) / (numOfVertices * (numOfVertices - 1))):.6f}')

        self._graphMatrix = graphMatrix
        self._numOfEdges = numOfEdges
        self._numOfVertices = numOfVertices
        self._vertices = np.arange(numOfVertices)

    def generateRandomVec(self, numOfColors):

        vec1 = np.arange(numOfColors)
        vec2 = np.random.randint(numOfColors, size=self._numOfVertices-numOfColors)
        vec = vec1 + vec2
        np.random.shuffle(vec)

        return vec.tolist()


    def calculateFitness(self, vec):
        sumOfViolations = 0

        for j in range(self._numOfVertices):
            for i in range(self._numOfVertices):
                if self._graphMatrix[i][j] and vec[i] == vec[j]:
                    sumOfViolations += 1

        return sumOfViolations

    def translateVec(self, vec):
        return vec

    def getVertices(self):
        return self._vertices.tolist()

    def getMostConstraintVariable(self, candidates, currSolution):
        # for MRV
        candidatesConstraintsWithAssigned = {}
        # For HD
        candidatesConstraintsWithUnassigned = {}

        for vertex in candidates:
            neighborsOfVertex = self.getNeighbors(vertex)
            constraintsWithAssigned = set()
            constraintsWithUnassigned = 0
            for nei in neighborsOfVertex:
                if nei in currSolution:
                    constraintsWithAssigned.add(currSolution[nei])
                else:
                    # prepare for HD
                    constraintsWithUnassigned += 1

            candidatesConstraintsWithAssigned[vertex] = constraintsWithAssigned
            candidatesConstraintsWithUnassigned[vertex] = constraintsWithUnassigned

        mostConstraintsVariables = []
        mostConstraints = -1
        for ver, constraintsWithAssigned in candidatesConstraintsWithAssigned.items():
            numOfConstraints = len(constraintsWithAssigned)
            if numOfConstraints > mostConstraints:
                mostConstraints = numOfConstraints
                mostConstraintsVariables = [ver]
            elif numOfConstraints == mostConstraints:
                mostConstraintsVariables.append(ver)

        if len(mostConstraintsVariables) == 1:
            return mostConstraintsVariables[0]

        # HD
        degreePerVer = {vertex: candidatesConstraintsWithUnassigned[vertex] for vertex in mostConstraintsVariables}
        return max(degreePerVer, key=degreePerVer.get)

    def getLeastConstrainingValue(self, vertex, currSol, verticesDomains):

        tempSol = currSol.copy()
        neighbors = [nei for nei in self.getNeighbors(vertex) if nei not in tempSol]
        leastConstraints = np.inf
        leastConstraintsValue = None

        for value in verticesDomains[vertex]:
            # assign the new value
            if self.isValidAssignment(vertex, value, tempSol):
                tempSol[vertex] = value
                # count constraints on neighbors
                constraints = set()
                for nei in neighbors:
                    neighborsOfNeiWithAssignment = [nei for nei in self.getNeighbors(nei) if
                                                    nei in tempSol and nei != vertex]
                    for neighborsOfNei in neighborsOfNeiWithAssignment:
                        if tempSol[neighborsOfNei] in verticesDomains[nei]:
                            constraints.add(tempSol[neighborsOfNei])

                numOfConstraints = len(constraints)
                if numOfConstraints < leastConstraints:
                    leastConstraints = numOfConstraints
                    leastConstraintsValue = value

        return leastConstraintsValue

    def isValidAssignment(self, vertex, wantedAssignment, otherAssignments: dict):
        for i in range(self._numOfVertices):
            if self._graphMatrix[vertex][i] and i in otherAssignments and otherAssignments[i] == wantedAssignment:
                return False

        return True

    def getNeighbors(self, vertex):
        neighbors = []
        for i in range(self._numOfVertices):
            if self._graphMatrix[vertex][i]:
                neighbors.append(i)

        return neighbors
