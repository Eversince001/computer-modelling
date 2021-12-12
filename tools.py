import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import f as hi2
import scipy.integrate as integrate
from scipy.special import gamma
import scipy.stats as stats
g_buf = ''
#график плотности распределения
def draw_graphs(pdf, params, interval=[0, 4]):
    a, b = interval

    #точки графика
    x = np.arange(a, b + 0.001, 0.001)

    if len(params) < 2:
        y = [pdf(point, params[0]) for point in x]
    else:
        y = [pdf(point, params[0], params[1]) for point in x]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(0, 1)
    ax.grid()
    ax.plot(x, y, linewidth=3, color='red')
    plt.show()

#графики эмпирической и теоретической функции плотности
def draw_empir_graphs(pdf, params, seq, interval=[0, 4]):
       
    #границы интервала для рисования
    a, b = interval
    
    #точки графика
    x = np.arange(a, b + 0.001, 0.001)
    
    #теоретический график
    if len(params) < 2:
        y = [pdf(point, params[0]) for point in x]
    else:
        y = [pdf(point, params[0], params[1]) for point in x]

    n = len(seq)
    
    #число интервалов
    K = int(5 * np.log10(n))
    
    #эмпирические значения
    weights, bins_edges = np.histogram(seq, bins=K, range=(a, b))

    #эмпирический график
    weights = np.array(weights) / n
    for i in range(len(weights)):
        weights[i] /= (bins_edges[i+1]-bins_edges[i])

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111) #1x1 grid, first subplot
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(0, 1)
    ax.grid()

    #вывод графика (эмпир)
    ax.hist(bins_edges[:-1], bins_edges, weights=weights, color='lightgray')
    
    #вывод графика (теор)
    ax.plot(x, y, linewidth=3, color='green')

    plt.xticks(bins_edges)
    ax.tick_params(axis='x', rotation=90)
    plt.show()

#критерий хи-квадрат
def chi2_test(seq, cdf, params, interval, alpha=0.05):
    global g_buf

    mu, sigma = params
    a, b = interval
    n = len(seq)
    K = int(5*np.log10(n)) #число интервалов

    weights, bins_edges = np.histogram(seq, bins=K, range=(a, b))
    weights = np.array(weights) / n

    S = 0
    for i in range(int(K)):
        P = cdf(bins_edges[i+1], mu, sigma) - cdf(bins_edges[i], mu, sigma)
        S += (weights[i] - P)**2 / P

    S = S * n

    print('Критерий \u03c7\u00b2')
    print('Число интервалов K: '+ str(K))
    print('Значение статистики хи-квадрат: ' + str(np.round(S, 3)))
    g_buf += 'Критерий \u03c7\u00b2\n'
    g_buf += 'Число интервалов K: ' + str(K) + '\n'
    g_buf += 'Значение статистики хи-квадрат: ' + str(np.round(S, 3)) + '\n'

    p = integrate.quad(lambda x: pow(x, (K - 1) / 2 - 1) * np.exp(-x / 2), S, math.inf)
    p /= pow(2, (K - 1) / 2) * gamma((K - 1) / 2)
    
    print('Достигнутый уровень значимости: ' + str(p[0]))
    g_buf += 'Достигнутый уровень значимости: ' + str(p[0]) + '\n'
    
    #критическое значение статистики
    S_a = stats.chi2.ppf(1-alpha, K-1)
    
    if p[0] < alpha:
        print('Гипотеза о согласии отвергается\n')
        g_buf += 'Гипотеза о согласии отвергается\n\n'
    else: 
        if S > S_a:
            print('Гипотеза о согласии отвергается\n')
            g_buf += 'Гипотеза о согласии отвергается\n\n'
        else:
            print('Гипотеза о согласии не отвергается\n')
            g_buf += 'Гипотеза о согласии не отвергается\n\n'

#вычисление значения I (для Крамера-Мизеса-Смирнова)
def I(z, v):
    res = 0
    for k in range(pow(2, 5)):
        res += pow(z/2, v+2*k)/(gamma(k+1)*gamma(k+v+1))
    return res

F = lambda x, n: x/ (n - 1)

#критерий Крамера-Мизеса-Смирнова
def cramer_mizes_smirnov_test(seq, cdf, params, N, alpha=0.05):
    global g_buf
    
    l=N/10
    seq = seq[:int(l)]
    n = len(seq)
    seq = np.sort(seq)

    #значение статистики
    S = 1 / (12*n)
    for i in range(n):
        if len (params) < 2:
            S += pow(cdf(seq[i], params[0]) - (2*(i+1)-1)/(2*n), 2)
        else:
            S += pow(cdf(seq[i], params[0], params[1]) - (2*(i+1)-1)/(2*n), 2)

    #достигнутый уровень значимости
    a1 = 0
    for j in range(pow(2, 6)):
        temp = (gamma(j+0.5)*np.sqrt(4*j+1))/(gamma(0.5)*gamma(j+1))
        temp *= np.exp(-pow(4*j+1, 2)/(16*S))
        temp *= (I(pow(4*j+1, 2)/(16*S), -0.25) - I(pow(4*j+1, 2)/(16*S), 0.25))
        a1 += temp
    a1 /= np.sqrt(2*S)

    p = 1 - a1
    
    #критическое значение статистики
    S_a = 0.4614
          
    print('Критерий \u03C9\u00b2-Крамера-Мизеса-Смирнова')
    print('Значение статистики: '+ str(np.round(S, 3)))
    print('Достигнутый уровень значимости: ' + str(np.round(p, 4)))
    g_buf += 'Критерий \u03C9\u00b2-Крамера-Мизеса-Смирнова' + '\n'
    g_buf += 'Значение статистики: '+ str(np.round(S, 3)) +'\n'
    g_buf += 'Достигнутый уровень значимости: ' + str(np.round(p, 4)) + '\n'
    
    if p < alpha:
        print('Гипотеза о согласии отвергается\n')
        g_buf += 'Гипотеза о согласии отвергается\n\n'
        return 0
    else: 
        if S > S_a:
            print('Гипотеза о согласии отвергается\n')
            g_buf += 'Гипотеза о согласии отвергается\n\n'
            return 0
        else:
            print('Гипотеза о согласии не отвергается\n')
            g_buf += 'Гипотеза о согласии не отвергается\n\n'
            return 1