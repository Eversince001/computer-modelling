from numpy import inf
import sympy as sm
import math
from scipy.integrate import quad
import workwithFiles


def a2(S):
    A2 = 0
    for i in range(20):
        arg = 4 * i + 1
        func = lambda x: math.e**(S/(8*(x**2 + 1)) - (arg**2 * math.pi**2 * x**2) / (8 * S))
        AZ = -1**i * ((math.gamma(i + 1/2) * arg) / (math.gamma(1/2) * math.gamma(i + 1)))
        AZ *= math.e**-((arg**2 * math.pi**2) / 8 * S)
        res = quad(func, 0, inf)
        AZ *= res[0]
        A2 += AZ 
    A2 *= math.sqrt(2 * math.pi) / S
    return A2

def AndersonDarling(x, n, m):
    content = []
    alpha = 0.015
    sortedX = sorted(x[:n:])
    S = 0

    for i in range(n):
        S +=((2 * i - 1)/(2 * n) * sm.ln(sortedX[i]/m) + (1 - (2 * i - 1)/(2 * n)) * sm.ln(1 - sortedX[i]/m))
    
    S = -n - 2 * S

    P = 1 - a2(S)

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

    