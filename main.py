from datetime import datetime
import math
import matplotlib.pyplot as plt
import timeit

from numpy import random
import workWithFiles
import numpy as np
import tools

args = tools.convert_param('args.txt')

random.seed()

start_time = datetime.now()

seq = tools.generator(args['N'])

seqV = tools.inv_generator(args, seq)

print('Время: ', datetime.now() - start_time)

#tools.plot_pdf_and_cdf(tools.exp_pdf, tools.exp_cdf, args, args['b'], args['a'])

#tools.plot_pdf_theoretical_and_empirical(tools.exp_pdf, args, seqV, args['b'], args['a'])

#tools.chi2_test(seqV, tools.exp_cdf, args, [args['a'], args['b']], args['alpha'])

#tools.kolmogorov(seqV, int(args['N']), args)