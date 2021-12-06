
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

def plot_pdf_and_cdf(pdf, cdf, args, xlims = 20, ylims={'pdf': 1, 'cdf': 1}):
    x = np.arange(0, xlims + 0.001, 0.001)
    print(x)
    y_pdf = [pdf(point, args) for point in x]
    y_cdf = [cdf(point, args) for point in x]

    fig, sub = plt.subplots(1, 2, figsize=(5, 5))
    fig.suptitle('Логистическое распределение с параметрами μ и v = {0} {1}'.format(int(args['u']), args['v']))
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


def plot_pdf_theoretical_and_empirical(pdf, args, sample, xlims = 20, ylims = 1):
    x = np.arange(0, xlims, 0.01)
    # Теоретические значения
    y = [pdf(point, args) for point in x]
    # Эмпирические значения
    weights, bin_edges = np.histogram(sample, range=(0, xlims), normed=True)
    # Создание полотна
    fig = plt.figure(figsize=(7, 5))
    fig.suptitle('Логистическое распределение с параметрами μ и v = {0} {1}'.format(int(args['u']), args['v'], len(sample)))
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

def smirnov(x, n, args):

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
    S = (6 * n * D + 1)**2 / (9 * n)
    print(f'Для {n}')
    print(f'S={S}')
    P = np.exp(-S / 2)
    print(f'P={P}')

    if(P > args['alpha']):
        print('Гипотеза Смирнова не отклоняется')
        return True # нет оснований для отклонения
    else:
        print('Гипотеза Смирнова отклоняется')
        return False # отклоняется








