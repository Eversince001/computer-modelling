import math
import scipy.integrate as integrate
from scipy.special import gamma
import scipy.stats as stats
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats.stats import _cdf_distance

def read_param(path):
    input = []
    with open(path) as file:
        for line in file:
            input.append(float(line))
    return input

def convert_param(path):
    args = {}
    input = []
    input = read_param(path)
    if (len(input) != 5):
        print('Wrong input value')
        raise Exception
    else:
        args = {
            'a': input[0],
            'b': input[1],
            'u': input[2],
            'N': input[3],
            'alpha': input[4],
        }
    return args

def generator(N):
    x = []
    for i in range(0, int(N)):
        x.append(random.uniform(0, 1))
    return x

def inv_generator(args, seq):
    tmp = []
    a = args['a']
    b = args['b']
    u = args['u']
    for i in range(0, len(seq)):
        x = seq[i]
        l = (u - a) / (b - a)
        if(x < 0 or x > 1):
            return 0
        elif(x >= 0 and x <= l):
            tmp.append(a + (b - a) * math.sqrt(l * x))
        elif(x <= 1 and x > l):
            tmp.append(b - (b - 1) * math.sqrt((1 - l) * x))
    
    tmp = np.random.triangular(int(args['a']), int(args['u']), int(args['b']), int( args['N']))

    return tmp

def plot_pdf_and_cdf(pdf, cdf, args, xlims, xmin, ylims={'pdf': 1, 'cdf': 1}):
    x = np.arange(xmin, xlims + 0.001, 0.001)
    print(x)
    y_pdf = [pdf(point, args) for point in x]
    y_cdf = [cdf(point, args) for point in x]

    fig, sub = plt.subplots(1, 2, figsize=(5, 5))
    fig.suptitle('Триангулярное распределение с параметрами a, b и μ = {0} {1} {2}'.format(int(args['a']), int(args['b']), int(args['u'])))
    titles = ['Функция плотности', 'Функция распределения']

    for ax, y, title, kind in zip(sub.flatten(), [y_pdf, y_cdf], titles, ['pdf', 'cdf']):
        # Органичение значений осей координат
        ax.set_xlim(xmin, xlims)
        ax.set_ylim(0, ylims[kind])
        # Разметка
        ax.grid()
        ax.set_title(title)
        ax.plot(x, y, color='green', linewidth=2)
    plt.show()

# функция плотности распределения
def exp_pdf(x, args):
    a = args['a']
    b = args['b']
    u = args['u']
    if(x >= a and x <= u):
         return (2 * (x - a)) / ((b - a) * (u - a))
    elif(x >= u and x <= b):
         return (2 * (b - x)) / ((b - a) * (b - u))


# Функция распределения
def exp_cdf(x, args):
    a = args['a']
    b = args['b']
    u = args['u']
    if(x <= a):
        return 0
    elif(x > a and x <= u):
        return (((x - a)**2) / ((b - a) * (u - a)))
    elif(x < b and x > u):
        return (1 - ((b - x)**2) / ((b - a) * (b - u)))
    elif(x >= b):
        return 1

def plot_pdf_theoretical_and_empirical(pdf, args, sample, xlims, xmin, ylims = 3):
    x = np.arange(xmin, xlims, 0.01)
    # Теоретические значения
    y = [pdf(point, args) for point in x]
    # Эмпирические значения
    weights, bin_edges = np.histogram(sample, range=(xmin, xlims), normed=True)
    # Создание полотна
    fig = plt.figure(figsize=(7, 5))
    fig.suptitle('Триангулярное распределение с параметрами a, b и μ = {0} {1} {2}'.format(int(args['a']), int(args['b']), int(args['u']), len(sample)))
    ax = fig.add_subplot(111)
    # Ограничение значений осей
    ax.set_xlim(xmin, xlims)
    ax.set_ylim(0, ylims)
    # Cетка
    ax.grid()
    # Вывод эмпирической функции
    plt.hist(bin_edges[:-1], bin_edges, weights=weights)
    # Вывод теоретической функции
    ax.plot(x, y, linewidth=3)
    # Значения оси Ox
    plt.xticks(bin_edges)
    plt.show()


def chi2_test(seq, cdf, args, interval, alpha):

    a, b = interval
    n = len(seq)
    K = int(5*np.log10(n)) #число интервалов

    weights, bins_edges = np.histogram(seq, bins=K, range=(a, b))
    weights = np.array(weights) / n

    S = 0
    for i in range(int(K)):
        P = cdf(bins_edges[i+1], args) - cdf(bins_edges[i], args)
        S += (weights[i] - P)**2 / P

    S = S * n

    print('Критерий \u03c7\u00b2')
    print('Число интервалов K: '+ str(K))
    print('Значение статистики хи-квадрат: ' + str(np.round(S, 3)))
   

    p = integrate.quad(lambda x: pow(x, (K - 1) / 2 - 1) * np.exp(-x / 2), S, math.inf)
    p /= pow(2, (K - 1) / 2) * gamma((K - 1) / 2)
    
    print('Достигнутый уровень значимости: ' + str(p[0]))
    
    #критическое значение статистики
    S_a = stats.chi2.ppf(1-alpha, K-1)
    
    if p[0] < alpha:
        print('Гипотеза о согласии отвергается\n')
    else: 
        if S > S_a:
            print('Гипотеза о согласии отвергается\n')
        else:
            print('Гипотеза о согласии не отвергается\n')



def calc_K(S):
    K = 0
    for k in range(-100, 10000):
        K += ((-1) ** k) * math.exp((-2 * k**2 * S**2))

    return K

def Dplus(x, n, args):
    maxD = 1/n-exp_cdf(x[0], args)

    for i in range(1,n):
        maxd = (i+1)/n - exp_cdf(x[i], args)
        if(maxd > maxD):
            maxD = maxd

    return maxD

def Dminus(x, n, args):
    maxD = exp_cdf(x[0], args)

    for i in range(1,n):
        maxd = exp_cdf(x[i], args) - i/n
        if(maxd > maxD):
            maxD = maxd

    return maxD

def kolmogorov(x, n, args):

    xsort = sorted(x)
    Dn = max([Dplus(xsort,n,args),Dminus(xsort,n,args)])
    Stat = (6 * n * Dn + 1) / (6 * np.sqrt(n))
    K = calc_K(Stat)

    p = 1 - K

    print("Проверка гипотезы о согласии с помощью Колмогорова:\n")
    print("Статистика: " + str(round(Stat,4)))
    print("Достигнутый уровень значимости: " + str(round(p,4)))
    print("Задаваемый уровень значимости: "+str(args['alpha']))

    result = ""

    if p > args['alpha']:
        result = "Гипотеза не отвергается"
    else:
        result = "Гипотеза отвергается"
        
    print(result)








