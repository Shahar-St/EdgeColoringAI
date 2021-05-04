import os

import numpy as np


class EdgeColoring:

    def __init__(self, fileName):
        print('Initiating input...')
        filePath = os.getcwd() + '\\util\\instances\\' + fileName
        inputFile = open(filePath, 'r')
        lines = [line[2:-1] for line in inputFile.readlines() if not line.startswith('c')]
        edgesAndVertices = lines[0].split(' ')[1:]
        numOfVertices = int(edgesAndVertices[0])
        numOfEdges = int(edgesAndVertices[1])
        graphMatrix = np.full((numOfVertices, numOfVertices), False)
        for edge in lines[1:]:
            vertices = edge.split(' ')
            graphMatrix[int(vertices[0]) - 1][int(vertices[1]) - 1] = True
            graphMatrix[int(vertices[1]) - 1][int(vertices[0]) - 1] = True

        maxDeg = 0
        for i in range(numOfVertices):
            vertexDeg = graphMatrix[i].sum()
            if vertexDeg > maxDeg:
                maxDeg = vertexDeg

        self._graphMatrix = graphMatrix
        self._numOfEdges = numOfEdges
        self._numOfVertices = numOfVertices
        self._vertices = np.arange(numOfVertices)
        self._maxDegree = maxDeg
        self._maxCliqueSize = self._getMaxCliqueSize(np.copy(graphMatrix), self._numOfVertices)

        print(f'Input File: {fileName}')
        print(f'# of edges: {numOfEdges}, # of vertices: {numOfVertices}')
        print(f'Graph density: {((2 * numOfEdges) / (numOfVertices * (numOfVertices - 1))):.6f}')
        print(f'Lower bound found: {self._maxCliqueSize}')
        print(f'Upper bound found: {self._maxDegree + 1}')

    def getNeighbors(self, vertex):
        neighbors = self._graphMatrix[vertex]
        return np.where(neighbors)[0]

    def generateRandomVec(self, numOfColors):
        vec1 = np.arange(numOfColors)
        vec2 = np.random.randint(numOfColors, size=self._numOfVertices - numOfColors)
        vec = np.concatenate((vec1, vec2))
        np.random.shuffle(vec)

        return vec

    def calculateFitness(self, vec):
        sumOfViolations = 0

        for i in range(self._numOfVertices):
            for j in range(i, self._numOfVertices):
                if self._graphMatrix[i][j] and vec[i] == vec[j]:
                    sumOfViolations += 1

        return sumOfViolations

    def translateVec(self, vec):
        if vec is None or self.calculateFitness(vec) != 0:
            return "Didn't find a valid solution"

        vec = self.shrinkColors(vec)
        numOfColors = len(set(vec))
        resStr = f'Number of colors: {numOfColors}.'
        if numOfColors == self.getLowerBound():
            resStr += ' This is an OPTIMAL SOLUTION!'
        resStr += '\nColor Classes:\n'

        for color in range(numOfColors):
            resStr += f'{color} =>'
            for vertex, verColor in enumerate(vec):
                if verColor == color:
                    resStr += f' {vertex},'
            resStr = resStr[:-1] + '.'
            resStr += '\n'

        return resStr

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

    def getNumOfVertices(self):
        return self._numOfVertices

    def getMaxDegree(self):
        return self._maxDegree

    def getUpperBound(self):
        return self._maxDegree + 1

    def getLowerBound(self):
        return self._maxCliqueSize

    def shrinkColors(self, vec):
        colorsUsed = len(set(vec))
        if colorsUsed == max(vec) - 1:
            return vec

        extraColors = set([color for color in vec if color >= colorsUsed])
        missingColors = [color for color in range(colorsUsed) if color not in vec]
        colorsMapping = dict(zip(extraColors, missingColors))
        adjustedVec = [color if color not in extraColors else colorsMapping[color] for color in vec]
        return adjustedVec

    # greedy algo, (will not always find the largest clique)
    def _getMaxCliqueSize(self, graphMatrix, verticesLeft):
        if verticesLeft == 1:
            return 1

        minDegVer = None
        minDeg = np.inf
        for i in range(self._numOfVertices):
            vertexDeg = graphMatrix[i].sum()
            if 0 < vertexDeg < minDeg:
                minDeg = vertexDeg
                minDegVer = i

        if minDeg == verticesLeft - 1:
            return minDeg + 1

        for v in range(self._numOfVertices):
            graphMatrix[minDegVer][v] = graphMatrix[v][minDegVer] = False

        return self._getMaxCliqueSize(graphMatrix, verticesLeft - 1)

    def _getMaxConflictedVertex(self, vec):
        maxNumConflicts = 0
        maxConflictedVertex = 0
        for vertex in range(self._numOfVertices):
            curNumConflicts = self._getVertexConflicts(vec, vertex)
            if curNumConflicts > maxNumConflicts:
                maxNumConflicts = curNumConflicts
                maxConflictedVertex = vertex

        return maxConflictedVertex

    def _getVertexConflicts(self, vec, vertex):
        numOfConflicts = 0
        neighborsList = self.getNeighbors(vertex)
        for nei in neighborsList:
            if vec[vertex] == vec[nei]:
                numOfConflicts += 1

        return numOfConflicts

    def generateSolutionNeighbors(self, vec, numOfColors):
        maxConflictedVertex = self._getMaxConflictedVertex(vec)
        neighbors = []
        for color in range(numOfColors):
            if color != vec[maxConflictedVertex]:
                nei = np.copy(vec)
                nei[maxConflictedVertex] = color
                neighbors.append(nei)

        return neighbors
