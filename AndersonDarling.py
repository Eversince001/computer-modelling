from numpy import inf
import sympy as sm
import numpy as np
import math
from scipy.integrate import quad
import workwithFiles


def a2(S):
    A2 = 0
    for i in range(100):
        #arg = 4 * i + 1
        func = lambda x: np.exp(S/(8*(x**2 + 1)) - ((4 * i + 1)**2 * np.pi**2 * x**2) / (8 * S))
        res = quad(func, 0, inf)[0]
        A2 += (-1)**i * (math.gamma(i + 1 / 2) * (4 * i + 1))/(math.gamma(1/2) * math.gamma(i + 1)) * np.exp(-((4 * i + 1)**2 * np.pi**2) / (8 * S)) * res

    A2 *= np.sqrt(2 * math.pi) / S
    return A2

def F(x, m):
    a = 0
    b = m
    return (x - a) / (b - a)

def AndersonDarling(x, n, m):
    content = []
    alpha = 0.05
    x.sort()
    S = 0

    for i in range(n):
        t = (2 * i - 1) / (2 * n)
        S += t * np.log(F(x[i], m)) + (1 - t) * np.log(1 - F(x[i], m))


    S = -n - 2 * S

    P = round(1 - a2(S), 200)

    content.append("\nTesting the agreement hypothesis using the nonparametric Anderson-Darling test\n\n" + str(n)) #Проверка гипотезы о согласии с помощью непараметрического критерия Андерсона-Дарлинга
    
    print("Testing the agreement hypothesis using the nonparametric Anderson-Darling test:\n") #Проверка гипотезы о согласии с помощью непараметрического критерия Андерсона-Дарлинга
    print("Achieved level of significance: " + str(P)) #Достигнутый уровень значимости
    print("Specified significance level: "+ str(alpha)) #Задаваемый уровень значимости
    
    if P > alpha:
         result = "The hypothesis is not rejected" #Гипотеза не отвергается
    else:
         result = "The hypothesis is rejected" #Гипотеза отвергается
    print(result)
    
    content.append("Achieved level of significance: " + str(P)) #Достигнутый уровень значимости
    content.append("Specified significance level: "+ str(alpha)) #Задаваемый уровень значимости
    content.append(result)
    
    workwithFiles.writeToFile("test.txt", content)

    return P

    