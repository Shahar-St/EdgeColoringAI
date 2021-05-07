import importlib
from abc import ABC, abstractmethod


# An abstract class that implements and declares common functionality to all algorithms
class Algorithm(ABC):

    def __init__(self, problem):
        self._problem = problem
        self._numOfSearchedStates = 0

    # This function should run the algorithm
    @abstractmethod
    def findSolution(self, maxIter):
        raise NotImplementedError

    @staticmethod
    def factory(algoName, popSize, problem, isHybrid):
        module = importlib.import_module('algorithms.' + algoName)

        algo = getattr(module, algoName)

        if algoName == 'GeneticAlgorithm':
            return algo(
                problem=problem,
                popSize=popSize,
            )
        elif algoName == 'FeasibleTabuSearch':
            return algo(
                problem=problem,
                isHybrid=isHybrid,
            )
        else:
            return algo(problem=problem)

