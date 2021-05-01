import psutil

GA_POP_SIZE = 200  # ga population size
GA_MAX_ITER = 200  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1
DEFAULT_TARGET = 'le450_25a.col'

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.2  # elitism rate
GA_MUTATION_RATE = 0.4  # mutation rate

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'Backtracking'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm', 'Backtracking')
