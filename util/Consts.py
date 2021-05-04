import psutil

GA_POP_SIZE = 30  # ga population size
GA_MAX_ITER = 200  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1
DEFAULT_TARGET = 'anna.col'

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.2  # elitism rate
GA_MUTATION_RATE = 0.4  # mutation rate

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'BackJumping'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm', 'BackJumping')
