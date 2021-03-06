import argparse
import time
import traceback

from algorithms.Algorithm import Algorithm
from problems.EdgeColoring import EdgeColoring
from problems.GeneticEdgeColoring import GeneticEdgeColoring
from util.Consts import *


def main():
    startTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', default=DEFAULT_ALGORITHM)
    parser.add_argument('-hb', '--isHybrid', default=DEFAULT_IS_HYBRID)
    parser.add_argument('-ps', '--popSize', type=int, default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET)

    args = parser.parse_args()

    # validate input
    if args.algo not in ALLOWED_ALGO_NAMES:
        print("invalid algo!\n")
        exit(1)

    # get params
    algoName = args.algo
    isHybrid = args.isHybrid
    popSize = args.popSize
    target = args.target

    if algoName == 'GeneticAlgorithm':
        problem = GeneticEdgeColoring(target)
    else:
        problem = EdgeColoring(target)

    algo = Algorithm.factory(algoName=algoName,
                             popSize=popSize,
                             problem=problem,
                             isHybrid=isHybrid
                             )

    # declare the run parameters
    print(
        '\nRun parameters:\n'
        f'Algorithm: {algoName}'
    )
    if algoName == 'TabuSearch':
        print(f'is hybrid function: {isHybrid}')
    if algoName == 'GeneticAlgorithm':
        print(f'Population Size: {popSize}')

    # find a solution and print it
    solVec, numOfStates = algo.findSolution(GA_MAX_ITER)
    print(f'\nSolution = {problem.translateVec(solVec)}')
    print(f'Number of searched states: {numOfStates}\n')

    # print summery of run
    endTime = time.time()
    elapsedTime = endTime - startTime
    print(f'Total elapsed time in seconds: {elapsedTime}')
    print(f'This process took {elapsedTime * CLOCK_RATE} clock ticks')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
