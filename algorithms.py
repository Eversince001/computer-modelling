import math
import numpy as np
import random
from scipy.integrate import quad
from scipy.stats import hypergeom
import matplotlib.pyplot as plt
from scipy.stats import chi2
import workWithFiles
from scipy.special import comb

def generator(n):
    seq = [0] * n

    for i in range(n):
        seq[i] = random.uniform(0, 1)

    return seq

def period(x):
 x1 = x[999]
 x2 = x[998]
 T = 2
 x_new = []
 for i in range(len(x) - 3, 1, -1):
    if(x[i] != x1):
        T+=1
    else:
        if(x[i-1]!=x2):
            T += 1
        else:
            break
    if(T > 100):
        for j in range(i, len(x)-1):
            x_new.append(x[j])
 return T, x_new

def chi_test(p, l):
    content = []
 # статистика
    alpha = 0.05
    S=0
    K = len(p)
    # теоретические вероятности
    # вероятность появления каждого уникального элемента
    P = [l ** k / math.factorial(k) * math.exp(-l) for k in range(K)] # р уже пронормированы по n
    for i in range(K):
        S = S + (p[i] - P[i])**2 / P[i]
    S = S * len(p)

    content.append('Statistics S = ' + str(np.round(S, 3)) + '\n')
    content.append('Statistics S crit = ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + '\n')
    print('Статистика S =', np.round(S, 3))
    print('Статистика S крит. =', np.round(chi2.ppf(1-alpha, K - 1), 3))

    if chi2.ppf(1-alpha, K - 1) > S:
        content.append(str(np.round(S, 3)) + ' < ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => chi-square hypothesis is not rejected' + '\n')
        workWithFiles.writeToFile("result.txt", content)
        print(np.round(S, 3), ' <', np.round(chi2.ppf(1-alpha, K - 1), 3), '=> гипотеза по хи-квадрат не отклоняется')
        pS = getChi2(S, K)
        print("Достигнутый уровень значимости = " + str(pS))
        return 1
    else:
        content.append(str(np.round(S, 3)) + ' > ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => chi-square hypothesis is rejected' + '\n')
        workWithFiles.writeToFile("result.txt", content)
        print(np.round(S, 3), ' >', np.round(chi2.ppf(1-alpha, K - 1), 3), '=> гипотеза по хи-квадрат отклоняется')
        pS = getChi2(S, K)
        print("Достигнутый уровень значимости = " + str(pS))
        return 0



    sum = 0 
    p = K/ N
    for i in range(1, n):
        sum = sum + 1
        if (Bernoulli(p) and sum == K):
            return sum
        p = (K - sum) / (N - i)
    return sum

def hypergeom_pmf(N, A, n, x):

    Achoosex = comb(A,x)
    NAchoosenx = comb(N-A, n-x)
    Nchoosen = comb(N,n)

    return (Achoosex)*NAchoosenx/Nchoosen

def degree_law(k, s, N, m):
    degree = []
    K = int(k/s)
    for j in range(0, K):
        for i in range(0, s):
            degree.append(hypergeom_pmf(N, m, s, i)) 

    return degree

def a(x, r):
    return x**(r/2-1) * math.exp(-x/2)

def getChi2(S,K):
    r = K-1
    gamma = math.gamma(r/2)* 2**(r/2)
    integ = quad(a, S, math.inf, args=(r,))
    return integ[0]/gamma

def chi_test_standart(p):
    content = []
    #статистика
    alpha = 0.05
    S=0
    K = len(p)
    S = 1
    Xi = list(set(p))
    for x in Xi:
        S += x * p.count(x) / len(p)
    
    content.append('Statistics S = ' + str(np.round(S, 3)) + '\n')
    content.append('Statistics S crit = ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + '\n')
    print('Статистика S = ', np.round(S, 3))
    print('Статистика S крит. = ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)))
    if chi2.ppf(1-alpha, K - 1) > S:
        content.append(str(np.round(S, 3)) + ' < ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => chi-square hypothesis is not rejected' + '\n')
        workWithFiles.writeToFile("result.txt", content)
        print(str(np.round(S, 3)) + ' < ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => гипотеза по хи-квадрат не отклоняется')
        pS = getChi2(S, K)
        print("Достигнутый уровень значимости = " + str(pS))
        return S
    else:
        content.append(str(np.round(S, 3)) + ' > ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => chi-square hypothesis is rejected' + '\n')
        print(str(np.round(S, 3)) + ' > ' + str(np.round(chi2.ppf(1-alpha, K - 1), 3)) + ' => гипотеза по хи-квадрат отклоняется')
        workWithFiles.writeToFile("result.txt", content)
        pS = getChi2(S, K)
        print("Достигнутый уровень значимости = " + str(pS))
        return S
  
def discret(p, n, s, N, m):
    content = []
    cnt = []
    content.append('Standart algorithm, n = ' + str(n) + '\n')
    workWithFiles.writeToFile("result.txt", content)
    degree = degree_law(n, s, N, m)
    res_seq = []
    for M in p:
        i = 1
        P = degree[1]
        while M >= 0 and i < n:
            M -= P
            i += 1
            P = degree[i]
        res_seq.append(i)


    #Определение эффективности алгоритма
    S = chi_test_standart(res_seq)
    K = math.ceil(S * len(res_seq))
    cnt.append('Count of itterations: ' + str(K) + '\n')
    print('Число иттераций: {0}\n'.format(K))
    weights = np.ones_like(res_seq) / len(res_seq)
    k = plt.hist(res_seq, weights=weights)
    plt.xlabel('k')
    plt.ylabel('Частота')
    title = 'Стандартный алгоритм при n = ' + str(n)
    plt.title(title)
    plt.show()
    cnt.append(str(res_seq) + '\n')
    workWithFiles.writeToFile("result.txt", cnt)
    return res_seq

def hyperg(values):

    N = values[0]
    m = values[1]
    s = values[2]
    rv = hypergeom(N, s, m)
    x = np.arange(0, s + 1)
    pmf = rv.pmf(x)

   
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, pmf, 'bo')
    ax.vlines(x, 0, pmf, lw=2)
    ax.set_xlabel('s')
    ax.set_ylabel('Частота')
    title = 'Теоретические частоты гипергеометрического закона закона при N = ' + str(N) + '\n' + 'm =' + str(m) + ' s = ' + str(s) 
    plt.title(title)
    plt.show()

def teor_puasson(n, l, K):
    
    puason = [l ** k / math.factorial(k) * math.exp(-l) for k in range(K)]
    plt.bar(np.arange(K), puason)
    plt.xticks(np.arange(K), np.arange(K))
    plt.xlabel('k')
    plt.ylabel('Частота')
    title = 'Теоретические частоты Пуассона при n = ' + str(n) + ', λ = ' + str(l)
    plt.title(title)
    plt.show()

def Puasson(l, n):
    # k - номер интервала
    puason = []
    P = lambda k: l ** k / math.factorial(k) * math.exp(-l) # находим вероятности до столбца с лямбдой
    i=0
    while i <= l:
        puason.append(P(i))
        i=i+1
    # завершаем хвост
    # пока текущая вероятность не станет меньше определенного значения
    while P(i) > 0.001:
        puason.append(P(i))
        i=i+1
    # в последний интервал поместим оставшуюся вероятность
    puason.append(1 - np.sum(puason[:len(puason)]))
    # суммы вероятностей
    return puason, i

def nestandart_alg(p_rav, n):
    content = []
    cnt = []
    content.append('Nonstandart algorithm, n = ' + str(n) + '\n')
    workWithFiles.writeToFile("result.txt", content)
    L = 5
    puason, K =  Puasson(L, n) # сумма с i = 0 до L включительно
    Q = np.sum(puason[:L+1])
    etta_ = np.zeros(K)
    res_seq = []
    iter = 0
    for alpha in p_rav:
        M = alpha - Q
        m = L
        P = puason[L]
        if M < 0:
            while True:
                M=M+P
                iter = iter + 1
                if M >= 0 or m == 0:
                    etta_[m] = etta_[m] + 1
                    res_seq.append(m)
                    break
                m = m - 1
                P = puason[m]
        elif M >= 0:
            while True:
                m = m + 1
                P = puason[m]
                iter = iter + 1
                if M <= 0 or m == n:
                    etta_[m-1] = etta_[m-1] + 1
                    res_seq.append(m-1)
                    break
                M = M - P

    cnt.append('Count of itterations: ' + str(iter) + '\n')
    cnt.append('Count of intervals K: ' + str(K) + '\n')
    print('Количество итераций:', iter)
    print('Число интервалов К:', K) #нормировка частот
    etta_ = etta_ / n
    # тест хи-квадрат
    chi_test(etta_, L)
    plt.bar(np.arange(K), etta_)
    plt.xticks(np.arange(K), np.arange(K))
    plt.xlabel('k')
    plt.ylabel('Частота')
    title = 'Нестандартный алгоритм при n = ' + str(n) + ', λ = ' + str(L)
    plt.title(title)
    plt.show()
    cnt.append(str(res_seq) + '\n')
    workWithFiles.writeToFile("result.txt", cnt)
    return res_seq, K