import psutil

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second
BEST = 0

GA_POP_SIZE = 10  # ga population size
GA_MAX_ITER = 200  # maximum iterations

DEFAULT_TARGET = 'le450_25a.col'

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.2  # elitism rate
GA_MUTATION_RATE = 0.4  # mutation rate

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'GeneticAlgorithm'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm', 'BackJumping', 'FeasibleTabuSearch', 'ObjectiveMinimizer', 'ForwardChecking')
