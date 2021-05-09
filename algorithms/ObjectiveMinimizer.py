import copy
import random

import numpy as np

from algorithms.Algorithm import Algorithm


class ObjectiveMinimizer(Algorithm):

    def __init__(self, problem):
        super().__init__(problem)

    def findSolution(self, maxIter):
        currentVec = self._problem.generateGreedyVec()
        currentColorClasses = self._problem.createColorClasses(currentVec)

        globalColorClasses = copy.deepcopy(currentColorClasses)
        globalObjectiveValue = self._problem.calculateObjectiveFunction(globalColorClasses)

        self._numOfSearchedStates += 1

        lowerBound = self._problem.getLowerBound()

        # iterative improvement
        iterCounter = 0
        while iterCounter < maxIter and len(globalColorClasses) > lowerBound:

            currentColorClasses = self.findNewSolution(currentColorClasses)
            currentObjectiveValue = self._problem.calculateObjectiveFunction(currentColorClasses)

            # check for best overall solution
            if currentObjectiveValue > globalObjectiveValue:
                globalObjectiveValue, globalColorClasses = currentObjectiveValue, currentColorClasses

            iterCounter += 1

        vec = self.colorClassToVec(globalColorClasses)
        numOfSearchedStates = self._numOfSearchedStates
        self._numOfSearchedStates = 0
        return vec, numOfSearchedStates

    def findNewSolution(self, colorClasses):
        self._numOfSearchedStates += 1
        colorClasses.sort()

        colorToRemoveFrom, colorToAddTo = self.getColorsToInterchange(colorClasses)
        vertex = self._problem.getMinimumDegVertexFromCandidates(colorClasses[colorToRemoveFrom].getVertices())
        colorClasses[colorToRemoveFrom].removeVertex(vertex)
        colorClasses[colorToAddTo].addVertex(vertex)

        self.kempeChains(colorClasses[colorToRemoveFrom], colorClasses[colorToAddTo], vertex)
        # remove empty classes
        for colorClass in colorClasses:
            if len(colorClass) == 0:
                colorClasses.remove(colorClass)

        return colorClasses

    # find 2 color classes to interchange
    def getColorsToInterchange(self, colorClasses):

        y = int(0.2 * len(colorClasses))
        index = random.randint(0, y)
        return index, len(colorClasses) - 1

    # make the 2 color classes a feasible solution
    def kempeChains(self, colorClassForPop, colorClassToAppend, movedVertex):

        neighbors = self._problem.getNeighbors(movedVertex)
        verticesOfPop = colorClassForPop.getVertices()
        verticesOfAppend = colorClassToAppend.getVertices()

        # find the intersection between vertices' neighbors and color classes' vertices
        intersection = list(set(verticesOfAppend) & set(neighbors))

        iterCount = 0
        while len(intersection) != 0:

            # check if to add vertex from 'colorClassForPop' to 'colorClassToAppend' or vice versa
            if iterCount % 2 == 0:
                verticesOfPop = verticesOfPop + intersection
            else:
                verticesOfAppend = verticesOfAppend + intersection

            neighbors = []
            for vertex in intersection:
                if iterCount % 2 == 0:
                    verticesOfAppend.remove(vertex)
                else:
                    verticesOfPop.remove(vertex)

                neighbors = neighbors + self._problem.getNeighbors(vertex).tolist()

            # find the intersection between vertices' neighbors and color classes' vertices
            if iterCount % 2 == 0:
                intersection = list(set(verticesOfPop) & set(neighbors))
            else:
                intersection = list(set(verticesOfAppend) & set(neighbors))

            colorClassToAppend.setVertices(verticesOfAppend)
            colorClassForPop.setVertices(verticesOfPop)

            iterCount += 1

    # translate color class to vector
    def colorClassToVec(self, listColorClasses):
        vec = np.empty(self._problem.getNumOfVertices())

        for colorClass in listColorClasses:
            color = colorClass.getColor()
            vertices = colorClass.getVertices()
            for vertex in vertices:
                vec[vertex] = color

        return vec
