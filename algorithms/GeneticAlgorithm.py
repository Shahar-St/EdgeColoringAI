import math
import random
import time

import numpy as np

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity

from util.Consts import BEST, CLOCK_RATE


# implements the genetic algorithm
class GeneticAlgorithm(Algorithm):

    def __init__(self, problem, popSize, eliteRate, mutationRate):
        super().__init__(problem, popSize)

        self._citizens = np.array(
            [IndividualEntity(problem.generateRandomVec()) for _ in
             range(popSize)])

        self._mean = None
        self._standardDeviation = None
        self._eliteRate = eliteRate
        self._mutationRate = mutationRate

    def findSolution(self, maxIter):

        # measure time
        totalRunTime = time.time()

        # init the fitness of the citizens
        self.updateFitness()
        best = self._citizens[BEST]

        # iterative improvement
        iterCounter = 0
        while best.getFitness() != 0 and iterCounter < maxIter:
            startTime = time.time()

            self._mate()

            self.updateFitness()
            best = self._citizens[BEST]
            iterCounter += 1

            elapsedTime = time.time() - startTime
            print(f'Best:\n{self._problem.translateVec(best.getVec())}({best.getFitness()}). Mean: {self._mean:.2f},'
                  f' STD: {self._standardDeviation:.2f}. Time in secs: {elapsedTime}. '
                  f'CPU clicks: {elapsedTime * CLOCK_RATE}\n')

        totalElapsedTime = time.time() - totalRunTime
        print(f'Total: Iterations: {iterCounter}. Elapsed Time in secs: {totalElapsedTime}.'
              f' CPU clicks: {totalElapsedTime * CLOCK_RATE}\n')

        return best.getVec()

    def _mate(self):

        # get elite
        tempPopulation = self._getElite()

        # get the candidates to be parents
        candidates = self._getCandidates(self._citizens)
        candidatesSize = len(candidates)

        # fill in the rest of the population
        while len(tempPopulation) < self._popSize:

            # choose parents and make child
            parent1 = candidates[random.randrange(candidatesSize)]
            parent2 = candidates[random.randrange(candidatesSize)]
            newChild = self._problem.crossover(parent1.getVec(), parent2.getVec())

            # mutation factor
            if random.random() < self._mutationRate:
                newChild.setVec(self._problem.mutate(newChild.getVec()))

            tempPopulation.append(newChild)

        self._citizens = np.array(tempPopulation)

    def updateFitness(self):
        fitnessValues = []
        for citizen in self._citizens:
            fitnessVal = self._problem.calculateFitness(citizen.getVec())
            citizen.setFitness(fitnessVal)
            fitnessValues.append(fitnessVal)

        # calculate mean and std of fitness function across all genes
        self._citizens.sort()
        self._mean = np.mean(fitnessValues)
        self._standardDeviation = np.std(fitnessValues)

    def _getElite(self):
        eliteSize = int(self._popSize * self._eliteRate)
        return self._citizens[:eliteSize].tolist()

    def _getCandidates(self, citizens):
        candidates = []
        fitnessSum = 0

        # calculate sum of fitness of all genes.
        for i in range(len(citizens)):
            fitnessSum += math.sqrt(citizens[i].getFitness())  # scaling with sqrt

        # calculate a proportional fitness for each gene.
        fitnessRate = []
        for i in range(len(citizens)):
            fitnessRate.append(math.sqrt(citizens[i].getFitness()) / fitnessSum)  # scaling with sqrt

        # at index i we sum up the fitnesses until index i.
        # flip the list - the lower the fitness, the better the solution.
        cumFitnessRate = list(np.cumsum(np.flip(fitnessRate)))

        # N(pop size) spins
        for j in range(len(cumFitnessRate)):
            r = random.random()

            i = 0
            found = False

            # find the index that matching to r and append it to candidates list.
            while i < len(cumFitnessRate) and not found:
                if r < cumFitnessRate[i]:
                    candidates.append(citizens[i])
                    found = True
                i += 1

        return np.array(candidates)
