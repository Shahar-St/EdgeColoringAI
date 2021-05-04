import copy
import math

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity


class FeasibleTabuSearch(Algorithm):

    def __init__(self, problem):
        super().__init__(problem)

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

        while fitness == 0 and numOfColors >= lowerBound:
            fitness, curVec = self.findSolutionWithNumOfColors(maxIter, numOfColors)
            if fitness == 0:
                print(f'Found solution with {numOfColors} colors')
                resVec = curVec
                numOfColors -= 1

        self._maxTabuSize = None
        self._tabuList = None

        numOfSearchedStates = self._numOfSearchedStates
        self._numOfSearchedStates = 0
        return resVec, numOfSearchedStates

    def findSolutionWithNumOfColors(self, maxIter, numOfColors):
        currentSol = IndividualEntity(self._problem.generateRandomVec(numOfColors))
        self._numOfSearchedStates += 1
        globalSolution = copy.deepcopy(currentSol)
        globalFitness = self._problem.calculateFitness(currentSol.getVec())

        # iterative improvement
        iterCounter = 0
        while globalFitness != 0 and iterCounter < maxIter:
            currentSol = self._findBestNeighbor(currentSol, numOfColors)
            if currentSol is None:
                return globalFitness, globalSolution.getVec()

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
            neighbors[i].setFitness(self._problem.calculateFitness(neighbors[i].getVec()))
        neighbors.sort()

        for nei in neighbors:
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
