import copy

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity


class TabuSearchAlgorithm(Algorithm):

    def __init__(self, problem, popSize, maxTabuSize):
        super().__init__(problem, popSize)

        self._problem = problem
        self._maxTabuSize = maxTabuSize
        self._tabuList = []

    def findSolution(self, maxIter):

        numOfColors = self._problem.getUpperBound()
        fitness = 0
        resVec = []
        while fitness == 0:
            fitness, curVec = self.findSolutionWithNumOfColors(maxIter, numOfColors)
            if fitness == 0:
                resVec = curVec
                numOfColors -= 1

        return resVec

    def findSolutionWithNumOfColors(self, maxIter, numOfColors):

        currentSol = IndividualEntity(self._problem.generateRandomVec(numOfColors))
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
