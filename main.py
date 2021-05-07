import argparse
import os
import time
import traceback

from algorithms.Algorithm import Algorithm
from algorithms.BackJumping import BackJumping
from algorithms.ForwardChecking import ForwardChecking
from problems.EdgeColoring import EdgeColoring
from problems.GeneticEdgeColoring import GeneticEdgeColoring
from util.Consts import *
from matplotlib import pyplot as plt


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

    algoName = ['ForwardChecking', 'BackJumping']
    targets = ['le450_25a', 'le450_25b', 'le450_25c', 'queen16_16', 'queen15_15']
    fc_timeList = []
    bj_timeList = []
    fc_NumOfStates = []
    bj_NumOfStates = []
    fc_results = []
    bj_results = []
    directory_in_str = 'C:\\Users\\User\\Desktop\\Lab in AI\\Labs\\Lab3\\EdgeColoringAI\\util\\instances'
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename == 'test.col':
            continue

        print(f'\n------------{filename}-------------')

        problem = EdgeColoring(filename)
        print('\nForwardChecking:')
        f_c_startTime = time.time()
        fc = ForwardChecking(problem)
        f_c_solVec, f_c_numOfStates = fc.findSolution(GA_MAX_ITER)
        fc_NumOfStates.append(f_c_numOfStates)
        fc_res = problem.calculateFitness(f_c_solVec)
        fc_numOfColors = len(set(f_c_solVec))
        if fc_res == 0:
            fc_results.append(fc_numOfColors)
        else:
            fc_results.append(-1)

        fc_time = time.time() - f_c_startTime
        fc_timeList.append(fc_time)
        print(f'Time= {fc_time:.2f} secs, states= {f_c_numOfStates}, colors={fc_res}')
        print('\nBackwardJumping:')
        b_j_startTime = time.time()
        bj = BackJumping(problem)
        b_j_solVec, b_j_numOfStates = bj.findSolution(GA_MAX_ITER)
        bj_NumOfStates.append(b_j_numOfStates)
        bj_res = problem.calculateFitness(b_j_solVec)
        bj_numOfColors = len(set(b_j_solVec))
        if bj_res == 0:
            bj_results.append(bj_numOfColors)
        else:
            bj_results.append(-1)

        bj_time = time.time() - b_j_startTime
        bj_timeList.append(bj_time)
        print(f'Time= {bj_time:.2f} secs, states= {b_j_numOfStates}, colors={bj_res}')

    back = 'BackJumping'
    title = 'BackJumping vs ForwardChecking - '
    forward = 'ForwardChecking'

    fig = plt.figure()
    plt.title(title + 'Time comparison')
    plt.scatter(range(len(fc_timeList)), fc_timeList, label=forward)
    plt.scatter(range(len(bj_timeList)), bj_timeList, label=back)
    plt.legend()
    fig.savefig('C:\\Users\\User\\Desktop\\Lab in AI\\Labs\\Lab3\\EdgeColoringAI\\plots\\fc vs bj - time')
    plt.close(fig)
    plt.clf()

    fig = plt.figure()
    plt.title(title + 'Number of searched states')
    plt.scatter(range(len(fc_NumOfStates)), fc_NumOfStates, label=forward)
    plt.scatter(range(len(bj_NumOfStates)), bj_NumOfStates, label=back)
    plt.legend()
    fig.savefig('C:\\Users\\User\\Desktop\\Lab in AI\\Labs\\Lab3\\EdgeColoringAI\\plots\\fc vs bj - states')
    plt.close(fig)
    plt.clf()

    fig = plt.figure()
    plt.title(title + 'Results quality')
    plt.scatter(range(len(fc_results)), fc_results, label=forward)
    plt.scatter(range(len(bj_results)), bj_results, label=back)
    plt.legend()
    fig.savefig('C:\\Users\\User\\Desktop\\Lab in AI\\Labs\\Lab3\\EdgeColoringAI\\plots\\fc vs bj - Results quality')
    plt.close(fig)
    plt.clf()

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
    if algoName == 'FeasibleTabuSearch':
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
