import random

import numpy as np

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity

from util.Consts import BEST


class GeneticAlgorithm(Algorithm):

    def __init__(self, problem, popSize, eliteRate, mutationRate):
        super().__init__(problem, popSize)

        self._numOfColors = problem.getUpperBound()
        self._citizens = np.array(
            [IndividualEntity(problem.generateRandomVec(self._numOfColors)) for _ in
             range(popSize)])

        self._eliteRate = eliteRate
        self._mutationRate = mutationRate

    def findSolution(self, maxIter):

        # init the fitness of the citizens
        self.updateFitness()
        bestSolution = None

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

        return bestSolution

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
            while i < len(genVec):
                if genVec[i] >= self._numOfColors:
                    genVec[i] = np.random.randint(self._numOfColors)
                i += 1
            gen.setVec(np.array(genVec))

        newCitizens = [IndividualEntity(self._problem.generateRandomVec(self._numOfColors)) for _ in
                       range(len(self._citizens) - len(eliteCitizens))]
        self._citizens = np.array(eliteCitizens + newCitizens)
        self.updateFitness()
