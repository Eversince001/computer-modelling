from datetime import datetime
import math
from numpy import random
import tools

args = tools.convert_param('args.txt')

random.seed()

start_time = datetime.now()

tools.generator(args)

seq = tools.gen(args['N'])

seqV = tools.inv_generator(args, seq)

print('Время: ', datetime.now() - start_time)

#tools.plot_pdf_and_cdf(tools.exp_pdf, tools.exp_cdf, args)

tools.plot_pdf_theoretical_and_empirical(tools.exp_pdf, args, seqV)

tools.chi2_test(seqV, tools.exp_cdf, args, [-2, 2], args['alpha'])

tools.Smirnov(seqV, int(args['N']), args)