import copy
import math

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity


class TabuSearch(Algorithm):

    def __init__(self, problem, isHybrid):
        super().__init__(problem)

        self._isHybrid = isHybrid
        self._maxTabuSize = None
        self._tabuList = None

    def findSolution(self, maxIter):
        # init params
        self._maxTabuSize = int(math.sqrt(self._problem.getNumOfEdges()))
        self._tabuList = []

        lowerBound = self._problem.getLowerBound()
        fitness = 0
        resVec = self._problem.generateGreedyVec()
        greedyColoring = len(set(resVec))
        upperBound = self._problem.getUpperBound()
        numOfColors = min(upperBound, greedyColoring)
        if greedyColoring <= upperBound:
            print(f'Saved {upperBound - greedyColoring} runs with a greedy solution')
        else:
            resVec = None

        # find a feasible solution for k colors, then try to find a feasible solution for k-1 colors
        iterCount = 0
        while fitness == 0 and numOfColors >= lowerBound and iterCount < maxIter:
            _, curVec = self.findSolutionWithNumOfColors(maxIter, numOfColors)
            fitness = self._problem.calculateFitness(curVec)
            if fitness == 0:
                print(f'Found solution with {numOfColors} colors')
                resVec = curVec
                numOfColors -= 1

            iterCount += 1

        self._maxTabuSize = None
        self._tabuList = None

        numOfSearchedStates = self._numOfSearchedStates
        self._numOfSearchedStates = 0
        return resVec, numOfSearchedStates

    # find a solution with a fitness function according to input (first approach or hybrid approach)
    def findSolutionWithNumOfColors(self, maxIter, numOfColors):
        currentSol = IndividualEntity(self._problem.generateRandomVec(numOfColors))
        self._numOfSearchedStates += 1
        globalSolution = copy.deepcopy(currentSol)

        if self._isHybrid:
            globalFitness = self._problem.calculateHybridFitness(currentSol.getVec())
        else:
            globalFitness = self._problem.calculateFitness(currentSol.getVec())

        # iterative improvement
        iterCounter = 0
        while self._problem.calculateFitness(globalSolution.getVec()) != 0 and iterCounter < maxIter:
            currentSol = self._findBestNeighbor(currentSol, numOfColors)
            if currentSol is None:
                return globalFitness, globalSolution.getVec()

            if self._isHybrid:
                currentFitness = self._problem.calculateHybridFitness(currentSol.getVec())
            else:
                currentFitness = self._problem.calculateFitness(currentSol.getVec())

            # check for best overall solution
            if currentFitness < globalFitness:
                globalSolution, globalFitness = copy.deepcopy(currentSol), currentFitness

            iterCounter += 1

        return globalFitness, globalSolution.getVec()

    # finding the best neighbor from all neighbors
    def _findBestNeighbor(self, currentSol, numOfColors):
        neighborsVectors = self._problem.generateSolutionNeighbors(currentSol.getVec(), numOfColors)
        self._numOfSearchedStates += len(neighborsVectors)
        neighbors = [IndividualEntity(vec) for vec in neighborsVectors]
        for i in range(len(neighbors)):
            if self._isHybrid:
                neighbors[i].setFitness(self._problem.calculateHybridFitness(neighbors[i].getVec()))
            else:
                neighbors[i].setFitness(self._problem.calculateFitness(neighbors[i].getVec()))
        neighbors.sort()

        for nei in neighbors:

            if self._isHybrid:
                if self._problem.calculateHybridFitness(nei.getVec()) < self._problem.\
                        calculateHybridFitness(currentSol.getVec()):
                    return nei
                elif nei not in self._tabuList:
                    self._addToTabuList(nei)
                    return nei

            else:
                if self._problem.calculateFitness(nei.getVec()) < self._problem.calculateFitness(currentSol.getVec()):
                    return nei
                elif nei not in self._tabuList:
                    self._addToTabuList(nei)
                    return nei

        return None

    # adding neighbor that its fitness worse than current to the tabu list
    def _addToTabuList(self, nei):
        if len(self._tabuList) >= self._maxTabuSize:
            self._tabuList.pop(0)
        self._tabuList.append(nei)
