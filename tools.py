import math
import scipy.integrate as integrate
from scipy.special import gamma
import scipy.stats as stats
import random
import numpy as np
import matplotlib.pyplot as plt

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
    if (len(input) != 4):
        print('Wrong input value')
        raise Exception
    else:
        args = {
            'u': input[0],
            'v': input[1],
            'N': input[2],
            'alpha': input[3],
        }
    return args

def getab(u, v):
    a = u - v * np.log(np.log(100))
    b = u - v * np.log(np.log(100 / 99))
    return [a, b]

def gen(N):
    x = []
    for i in range(0, int(N)):
        x.append(random.uniform(0, 1))
    return x

def generator(args):
    u = int(args['u'])
    v = args['v']
    answer = []
    ab = getab(u,v)
    x = 0
    i = 0
    M = exp_pdf(u, args)
    countp = 0

    while i < args['N']:
        p1 = random.uniform(0, 1)
        p2 = random.uniform(0, 1)
        countp+=2
        x = ab[0] + p1 * (ab[1] - ab[0])
        y = p2 * M

        if (y < exp_pdf(x, args)):
            answer.append(x)
            i+=1

    print("Количество сгенерированных равномернораспределенных псевдослучайных величин ", countp)

    print("M = ", M)

    return answer

def plot_pdf_and_cdf(pdf, cdf, args, xlims = 6, ylims={'pdf': 1.5, 'cdf': 1}):
    x = np.arange(1, xlims + 0.001, 0.001)
    print(x)
    y_pdf = [pdf(point, args) for point in x]
    y_cdf = [cdf(point, args) for point in x]

    fig, sub = plt.subplots(1, 2, figsize=(5, 5))
    fig.suptitle('Логистическое распределение с параметрами μ и v = {0} {1}'.format(int(args['u']), args['v']))
    titles = ['Функция плотности', 'Функция распределения']

    for ax, y, title, kind in zip(sub.flatten(), [y_pdf, y_cdf], titles, ['pdf', 'cdf']):
        # Органичение значений осей координат
        ax.set_xlim(1, xlims)
        ax.set_ylim(0, ylims[kind])
        # Разметка
        ax.grid()
        ax.set_title(title)
        ax.plot(x, y, color='green', linewidth=2)
    plt.show()

# функция плотности распределения
def exp_pdf(x, args):
    u = args['u']
    v = args['v']

    return (np.exp(-(x - u) / v))/(v * (1 + np.exp(-(x - u) / v))**2)

# Функция распределения
def exp_cdf(x, args):
    u = args['u']
    v = args['v']
    
    return 1 / (1 + np.exp(-(x - u) / v))

def inv_generator(args, seq):
    tmp = []
    u = args['u']
    v = args['v'] 
    for x in seq:
        alpha = x
        tmp.append(- v * np.log(1 / alpha - 1) + u)

    return tmp

def plot_pdf_theoretical_and_empirical(pdf, args, sample, xlims = 6, ylims = 1.5):
    x = np.arange(2.5, xlims, 0.01)
    # Теоретические значения
    y = [pdf(point, args) for point in x]
    # Эмпирические значения
    weights, bin_edges = np.histogram(sample, range=(2.5, xlims), normed=True)
    # Создание полотна
    fig = plt.figure(figsize=(7, 5))
    fig.suptitle('Логистическое распределение с параметрами μ и v = {0} {1}'.format(int(args['u']), args['v'], len(sample)))
    ax = fig.add_subplot(111)
    # Ограничение значений осей
    ax.set_xlim(2.5, xlims)
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

    mu, sigma = args['u'], args['v']
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

def Smirnov(x, n, args):

    xsort = sorted(x)
    Dn = max([Dplus(xsort,n,args),Dminus(xsort,n,args)])
    Stat = (6*n*Dn + 1)**2 / (9*n)
    p = np.exp(-Stat/2)

    print("Проверка гипотезы о согласии с помощью Смирнова:\n")
    print("Статистика: " + str(round(Stat,4)))
    print("Достигнутый уровень значимости: " + str(round(p,4)))
    print("Задаваемый уровень значимости: "+str(args['alpha']))

    result = ""

    if p > args['alpha']:
        result = "Гипотеза не отвергается"
    else:
        result = "Гипотеза отвергается"
        
    print(result)








