import argparse
import time
import traceback

from algorithms.Algorithm import Algorithm
from problems.EdgeColoring import EdgeColoring
from util.Consts import *


def main():
    startTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', default=DEFAULT_ALGORITHM)
    parser.add_argument('-ps', '--popSize', type=int, default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET)

    args = parser.parse_args()

    # validate input
    if args.algo not in ALLOWED_ALGO_NAMES:
        print("invalid algo!\n")
        exit(1)

    # get params
    algoName = args.algo
    popSize = args.popSize
    target = args.target
    problem = EdgeColoring(args.target)

    algo = Algorithm.factory(algoName=algoName,
                             popSize=popSize,
                             eliteRate=GA_ELITE_RATE,
                             mutationRate=GA_MUTATION_RATE,
                             problem=problem
                             )

    # declare the run parameters
    print(
        '\nRun parameters:\n'
        f'Target: {target}\n'
        f'Algo: {algoName}\n'
    )

    # find a solution and print it
    solVec = algo.findSolution(GA_MAX_ITER)
    print(f'Solution = {problem.translateVec(solVec)}\n')

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
