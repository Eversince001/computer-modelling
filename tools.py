import math
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

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

def generator(N, b):
    x = []
    for i in range(0, int(N)):
        x.append(random.uniform(0, b))
    return x

def inv_generator(args, seq):
    tmp = []
    a = args['a']
    b = args['b']
    u = args['u']
    for i in range(0, len(seq)):
        alpha, x = seq[i], seq[i]
        if(x >= a and x <= u):
            tmp.append(math.sqrt(alpha * (b - a) * (u - a) + a**2) + a)
        elif(x >= u and x <= b):
            tmp.append(math.sqrt(alpha * (b - a) * (b - u) + b**2) + b)
        else:
            tmp.append(0)
    return tmp

def plot_pdf_and_cdf(pdf, cdf, args, xlims, ylims={'pdf': 1, 'cdf': 1}):
    x = np.arange(0, xlims + 0.001, 0.001)
    print(x)
    y_pdf = [pdf(point, args) for point in x]
    y_cdf = [cdf(point, args) for point in x]

    fig, sub = plt.subplots(1, 2, figsize=(5, 5))
    fig.suptitle('Триангулярное распределение с параметрами a, b и μ = {0} {1} {2}'.format(int(args['a']), int(args['b']), int(args['u'])))
    titles = ['Функция плотности', 'Функция распределения']

    for ax, y, title, kind in zip(sub.flatten(), [y_pdf, y_cdf], titles, ['pdf', 'cdf']):
        # Органичение значений осей координат
        ax.set_xlim(0, xlims)
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
    else:
        return 0

# Функция распределения
def exp_cdf(x, args):
    a = args['a']
    b = args['b']
    u = args['u']
    if(x >= a and x <= u):
        return (x*(x - 2*a))/((b - a)*(u - a))
    elif(x >= u and x <= b):
        return ((x*(x - 2*b))/((b - a)*(b - u)))
    else:
        return 0

def plot_pdf_theoretical_and_empirical(pdf, args, sample, xlims, ylims = 3):
    x = np.arange(0, xlims, 0.01)
    # Теоретические значения
    y = [pdf(point, args) for point in x]
    # Эмпирические значения
    weights, bin_edges = np.histogram(sample, range=(0, xlims), normed=True)
    # Создание полотна
    fig = plt.figure(figsize=(7, 5))
    fig.suptitle('Триангулярное распределение с параметрами a, b и μ = {0} {1} {2}'.format(int(args['a']), int(args['b']), int(args['u']), len(sample)))
    ax = fig.add_subplot(111)
    # Ограничение значений осей
    ax.set_xlim(0, xlims)
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


def chi_test(x, n, K, alpha):

    x_new = []

    for i in range(n):
        x_new.append(x[i])

    weights = np.ones_like(x_new) / len(x_new)
    S = 0
    P = 1 / K

    plt.ylabel('Частота')
    plt.xlabel('Интервалы')
    kint = plt.hist(x_new, int(K), weights=weights)

    for i in range(int(K)):
        S = S + (kint[0][i] - P)**2 / P

    S = S * len(x)

    print(f'Для {n}')
    print(f'S={S}')
    plt.show()
    ur = scipy.stats.chi2.ppf(1-alpha, K - 1)
    print(f'Уровень значимости = {ur}')
    if ur > S:
        print('Гипотеза по хи-квадрат не отклоняется')
        return True #гипотеза по хи-квадрат не отклоняется

    else:
        print('Гипотеза по хи-квадрат отклоняется')
        return False #гипотеза по хи-квадрат отклоняется


F = lambda x, n: x/ (n - 1)

def calc_K(S):
    K = 0
    for i in range(-100, 10000):
        K += ((-1) ** i) * math.exp((-2 * (i**2) * (S**2)))

    return K

def kolmogorov(x, n, args):

    x_new = []
    for i in range(n):
        x_new.append(x[i])

    x_new.sort()

    D_minus = []
    D_plus = []
    i = 1

    for x in x_new:
        D_minus.append(F (x, n) - (i - 1) / n)
        D_plus.append(i / n - F(x, n))
        i = i + 1

    D_p = max(D_plus)
    D_m = max(D_minus)
    D = max(D_p, D_m)
    S = (6 * n * D + 1) / (6 * np.sqrt(n))
    K = calc_K(S)
    print(f'Для {n}')
    print(f'S={S}')
    P = 1 - K
    print(f'P={P}')

    if(P > args['alpha']):
        print('Гипотеза по Колмагорова не отклоняется')
        return True # нет оснований для отклонения
    else:
        print('Гипотеза по Колмагорова отклоняется')
        return False # отклоняется










