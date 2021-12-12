import numpy as np
import math
import timeit
import matplotlib.pyplot as plt
from scipy.stats import f as hi2
from scipy.special import gamma
import random
import scipy.stats as stats
import tools

g_buf = ''

input = open('args.txt', 'r')
for line in input:
    n = int(line.split(' ')[0])


#графики теоретиических плотностей распределения
tools.draw_graphs(pdf=stats.norm.pdf, params=[0, 1], interval=[-3, 3])
tools.draw_graphs(pdf=stats.chi2.pdf, params=[n], interval=[0, 35])

for N in [50, 200, 1000]:
    print('Длина основной генерируемой последовательности N = ' + str(N) + '\n')
    g_buf += 'Длина основной генерируемой последовательности N = ' + str(N) + '\n\n'

    norm_seq = []
    beta_seq = []
    X_seq = []

    #замер времени (начало)
    start_time = timeit.default_timer()

    #моделирование стандартной нормальной величины методом Мюллера
    kol = N
    while(len(norm_seq)!=kol):
        ro1 = np.random.uniform(0, 1)
        ro2 = np.random.uniform(0, 1)

        eps1 = np.sqrt(-2*np.log(ro1))*np.cos(2*np.pi*ro2)
        eps2 = np.sqrt(-2*np.log(ro2))*np.sin(2*np.pi*ro1)

        norm_seq.append(eps1)
        norm_seq.append(eps2)
           
    chi2_n = []
        
    #моделирование распределения хи-квадрат
    for i in range(N):
        
        tmp = 0
        for j in range(n):
            p = np.random.normal(0, 1)
            tmp += pow(p, 2)
        chi2_n.append(tmp)

    for i in range(int(N)):
        ksi = 0
        for j in range(int(n)):
            p = random.uniform(0, 1)
            ksi += math.log(p)
        ksi *= -1
        X_seq.append(ksi)

    #замер времени (конец)
    totalTime = timeit.default_timer() - start_time
    
    print('Время моделирования выборки из '+ str(N) +' элементов: '+ str(round(totalTime, 5)))
    g_buf += 'Время моделирования выборки из '+ str(N) +' элементов: '+ str(round(totalTime, 5)) + '\n'
    
    #вывод информации о последовательности, полученной методом Мюллера
    print('----------------------------------------------')
    print('Нормальное распределение с параметрами: \u03BC = {0}; \u03C3 = {1}'.format(0, 1))
    print('Равномерно распределенных величин потребовалось: {0}\n'.format(N))
    print('Первые 50 элементов выборки:\nX={', end='')
    for i in range(50):
        print(np.round(norm_seq[i], 3), end=' ')
    print('}')
    
    g_buf += 'Нормальное распределение с параметрами: n = {0}; \u03C3 = {1}'.format(0, 1) + '\n'
    g_buf += 'Равномерно распределенных величин потребовалось: {0}\n'.format(N) + '\n'
    g_buf += 'Выборка: \n' + str(norm_seq) + '\n'
    
    tools.draw_empir_graphs(pdf=stats.norm.pdf, params=[0,1], seq=norm_seq, interval=[-4, 4])
    tools.chi2_test(seq=norm_seq, cdf=stats.norm.cdf, interval=[-2, 2], params=[0, 1])
    tools.cramer_mizes_smirnov_test(seq=norm_seq, cdf=stats.norm.cdf, params=[0, 1], N=N)
    
    #вывод информации о хи-квадрат распределении (n)
    print('----------------------------------------------')
    print('Хи-квадрат распределение с параметрами: k = {0}\n'.format(n))
    print('Нормально распределенных величин потребовалось: {0}\n'.format(N*n))
    print('Первые 50 элементов выборки:\nX={', end='')
    for i in range(50):
        print(np.round(chi2_n[i], 3), end=' ')
    print('}')
    
    g_buf += 'Хи-квадрат распределение с параметрами: k = {0}\n'.format(n) + '\n'
    g_buf += 'Нормально распределенных величин потребовалось: {0}\n'.format(N*n) + '\n'
    g_buf += 'Выборка: \n' + str(chi2_n) + '\n\n'
    
    tools.draw_empir_graphs(pdf=stats.chi2.pdf, params=[n], seq=chi2_n, interval=[0, 35])
    tools.chi2_test(seq=chi2_n, cdf=stats.chi2.cdf, params=[n, 0], interval=[0, 10])
    tools.cramer_mizes_smirnov_test(seq=chi2_n, cdf=stats.chi2.cdf, params=[16, 0], N=N)
    
    
    #вывод информации о сгенерированном распределении хи-квадрат
    print('----------------------------------------------')
    print('Распределение хи-квадрат с параметрами: n = {0}'.format(n))
    print('Первые 50 элементов выборки:\nX={', end='')
    for i in range(50):
        print(np.round(X_seq[i], 3), end=' ')
    print('}')
    
    g_buf += 'Распределение хи-квадрат с параметрами: n = {0}'.format(n) + '\n\n'
    g_buf += 'Выборка: \n' + str(X_seq) + '\n\n'
    
    tools.draw_empir_graphs(pdf=stats.chi2.pdf, params=[n], seq=X_seq, interval=[0, 35])
    tools.chi2_test(seq=X_seq, cdf=stats.chi2.cdf, params=[n, 0], interval=[0, 10])
    tools.cramer_mizes_smirnov_test(seq=X_seq, cdf=stats.chi2.cdf, params=[16, 0], N=N)

#записываем файл с результатами тестов
f = open('KM_RGZ_results.txt', 'w', encoding='utf-8')
f.write(g_buf)
f.close()