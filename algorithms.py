import scipy
import math
import random
from collections import Counter

def builtInGenerator(n):
    seq = [0] * n

    for i in range(n):
        seq[i] = random.random()

    return seq


#Гипергеометрическое распределение 
def HypergeometricDistribution(n, values):
    seq = [0] * n

    for k in range(values[2]):
            C1 = math.factorial(values[1])/(math.factorial(values[1] - k) *  math.factorial(k))
            C2 = math.factorial(values[0] - values[1])/(math.factorial(values[0] - values[1] - (values[2] - k)) *  math.factorial(values[2] - k))
            C3 = math.factorial(values[0])/(math.factorial(values[0] - values[2]) *  math.factorial(values[2]))
            seq[k] = (C1 * C2) / C3

    return seq

# Стандартный алгоритм
def standardAlgorithm(s, sP):
    n = len(s)
    ksi = [0] * n
    iters = [1] * n

    for i in range(n):
        m = s[i]
        k = 0
        m = m - sP[k]
        while m >= 0:
            iters[i] += 1
            k+=1
            m = m - sP[k]
        ksi[i] = k



    print("Кси: " + str(ksi) + "\n")
    print("Итерации: " + str(iters) + "\n")
    print("Всего: " + str(sum(iters)) + "\n")

    return ksi


# Нестандартный алгоритм
def nonStandardAlgorithm(s, sP, lmbd):
    n = len(s)
    ksi = [0] * n
    iters = [1] * n
    l = lmbd
    q = 0

#получим крайний слева
    i = 0
    while n*sP[i] <= 1:
        i += 1
    left = i
    
    
# получим крайний справа
    i = int(lmbd)
    while n * sP[i] > 1:
        i += 1
    right = i
    
    
    for i in range(l):
        q += sP[i]

    for i in range(n):
        p = sP[l]
        m = l
        mm = s[i] - q
        

        if mm < 0:
            mm = mm + p
            

            while mm < 0:
                iters[i] += 1
                if (m == left):
                    break
                m = m-1
                p = sP[m]
                mm = mm + p
            
            ksi[i] = m
                
        else:
            while mm >= 0:
                iters[i] += 1
                if (m == right):
                    break
                m = m + 1
                p = sP[m]
                mm = mm - p
            ksi[i] = m  
        
    print("Кси: " , ksi , "\n")
    print("Итерации: " , iters , "\n")
    print("Всего: " + str(sum(iters)) + "\n")

    return ksi


# Попадение в интервалы
def makeDict(ksi):
    counts = Counter(ksi)
    for i in counts.keys():
        counts[i] /= len(ksi)
    minD = min(counts.keys()) 
    maxD = max(counts.keys())
    for i in range(minD, maxD):
        if (i not in counts.keys()):
            counts[i] = 0
    return counts      


# Хи-квадрат, вычисление значения статистики 
def findChi2Stat(dictionary, sP):
    
    #sum -  статистика
    #sumP - сумма вероятностей, чтоб вычислить в последнем интервале вероятность
    sum = 0
    minD = min(dictionary.keys())
    sumP1 = 0
    for i in range(minD):
        sumP1 += sP[i]
    if (sumP1 > 0):
        sum += (dictionary[minD] - sumP1)**2/ sumP1
    
    sumP = 0
    lis = list(dictionary.keys())
    for i in range(len(lis)):
        elem = dictionary[lis[i]]
        sum += (elem - sP[lis[i]])**2/ sP[lis[i]]
        sumP += sP[lis[i]]
    sumP = 1 - sumP - sumP1
    sum -= (dictionary[i] - sP[lis[i]])**2/sP[lis[i]]
    sum += (dictionary[i] - sumP)**2/sumP
    sum *= len(list(dictionary.keys()))
    return sum


def a(x, r):
    return x**(r/2-1) * math.exp(-x/2)

# Хи-квадрат, вычисление достигнутого уровня значимости
def getChi2(S,K):
    r = K-1
    gamma = math.gamma(r/2)* 2**(r/2)
    integ = scipy.integrate.quad(a, S, math.inf, args=(r,))
    return integ[0]/gamma


#Эффективность для стандартного алгоритма
def mx(seq, sP):
    x = 1
    for i in seq:
        x += i*sP[i]
    return x

def q(i,lmbd):
    if (i > int(lmbd)):
        return lmbd - int(lmbd)
    else:
        return 1 - lmbd  + int(lmbd)
  
# Эффективность для нестандартного    
def mxH(seq, sP, lmbd):
    mx = 1
    for i in seq:
        s = 1 + abs(lmbd - i) + q(i, lmbd)
        mx += s * sP[s]
    return mx
