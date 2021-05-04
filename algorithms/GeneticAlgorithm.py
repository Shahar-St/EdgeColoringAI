import random

import numpy as np

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity

from util.Consts import BEST


class GeneticAlgorithm(Algorithm):
    ELITE_RATE = 0.2  # elitism rate
    MUTATION_RATE = 0.4  # mutation rate

    def __init__(self, problem, popSize):
        super().__init__(problem)

        self._popSize = popSize
        self._eliteRate = GeneticAlgorithm.ELITE_RATE
        self._mutationRate = GeneticAlgorithm.MUTATION_RATE
        self._numOfColors = None
        self._citizens = None

    def findSolution(self, maxIter):

        # init the fields
        bestSolution = self._problem.generateGreedyVec()
        greedyColoring = len(set(bestSolution))
        upperBound = self._problem.getUpperBound()
        self._numOfColors = min(upperBound, greedyColoring)
        if greedyColoring <= upperBound:
            print(f'Saved {upperBound - greedyColoring} runs with a greedy solution')
        else:
            bestSolution = self._problem.generateRandomVec(self._numOfColors)

        self._citizens = np.array(
            [IndividualEntity(self._problem.generateRandomVec(self._numOfColors)) for _ in
             range(self._popSize - 1)] + [IndividualEntity(bestSolution)])
        self.updateFitness()
        self._numOfSearchedStates = self._popSize

        # iterative improvement
        iterCounter = 0
        lowerBound = self._problem.getLowerBound()
        while iterCounter < maxIter and self._numOfColors >= lowerBound:
            self._mate()

            self.updateFitness()
            best = self._citizens[BEST]
            if best.getFitness() == 0:
                print(f'Found coloring with {self._numOfColors} colors. Iter: {iterCounter}')
                bestSolution = self._problem.shrinkColors(best.getVec()).copy()
                self._adjustPopulationToNewColor(bestSolution)
            iterCounter += 1

        # clean up
        self._numOfColors = None
        self._citizens = None
        numOfSearchedStates = self._numOfSearchedStates
        self._numOfSearchedStates = 0
        return bestSolution, numOfSearchedStates

    def _mate(self):
        # get elite
        tempPopulation = self._getElite()

        # get the candidates to be parents
        candidates = self._getCandidates()
        candidatesSize = len(candidates)

        # fill in the rest of the population
        while len(tempPopulation) < self._popSize:

            # choose parents and make child
            parent1 = candidates[random.randrange(candidatesSize)]
            parent2 = candidates[random.randrange(candidatesSize)]
            newChild = IndividualEntity(self._problem.crossover(parent1.getVec(), parent2.getVec()))

            # mutation factor
            if random.random() < self._mutationRate:
                newChild.setVec(self._problem.mutate(newChild.getVec(), self._numOfColors))
            self._numOfSearchedStates += 1
            tempPopulation.append(newChild)

        self._citizens = np.array(tempPopulation)

    def updateFitness(self):
        fitnessValues = []
        for citizen in self._citizens:
            fitnessVal = self._problem.calculateFitness(citizen.getVec())
            citizen.setFitness(fitnessVal)
            fitnessValues.append(fitnessVal)

        self._citizens.sort()

    def _getElite(self):
        eliteSize = int(self._popSize * self._eliteRate)
        return self._citizens[:eliteSize].tolist()

    def _getCandidates(self):
        citizensSize = len(self._citizens)
        candidates = []

        # get half the population
        for i in range(int(citizensSize / 2)):
            candidates.append(self._citizens[i])

        return np.array(candidates)

    def _adjustPopulationToNewColor(self, bestSolution):
        numOfColorsUsed = len(set(bestSolution))
        if numOfColorsUsed != self._numOfColors:
            print(f'saved {self._numOfColors - numOfColorsUsed} iterations')
        self._numOfColors = numOfColorsUsed - 1

        eliteCitizens = self._getElite()
        for gen in eliteCitizens:
            genVec = gen.getVec().tolist()
            genVec = self._problem.shrinkColors(genVec)
            i = 0
            changed = False
            while i < len(genVec):
                if genVec[i] >= self._numOfColors:
                    genVec[i] = np.random.randint(self._numOfColors)
                    changed = True
                i += 1
            if changed:
                self._numOfSearchedStates += 1
            gen.setVec(np.array(genVec))

        newCitizens = [IndividualEntity(self._problem.generateRandomVec(self._numOfColors)) for _ in
                       range(len(self._citizens) - len(eliteCitizens))]
        self._numOfSearchedStates += len(self._citizens) - len(eliteCitizens)
        self._citizens = np.array(eliteCitizens + newCitizens)
        self.updateFitness()
