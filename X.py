import math
import scipy
import tools
import workwithFiles

def X(x,n,k):
    counter = 0
    content = []
    alpha = 0.05
    intervals = [[0] * 2 for i in range(k)]
    p=[0]*k
    nin = [0]*k
    m = max(x[:n+1:]) - min(x[:n+1:])
    countInInterval = [0] * k
    
    for i in range(k):
        intervals[i][0] = counter
        intervals[i][1] = round(m/k + counter,2)
        counter =  intervals[i][1]
        
        for j in range(n):
            if intervals[i][0] <= x[j] < intervals[i][1]:
                countInInterval[i] += 1
        
        p[i] = (intervals[i][1]-intervals[i][0])/m
        nin[i] = countInInterval[i]/n
    
    sChi = 0
    for i in range(k):
        sChi += ((nin[i] - p[i])**2)/p[i]
    sChi *= n
    r = k - 1
    pSchi = 1/(2**(r/2)*math.gamma(r/2))
    pSchi1, err = scipy.integrate.quad(lambda xx: xx**(r/2 - 1)*math.exp(-xx/2), sChi, 1000)
    pSchi = pSchi*pSchi1
    
    content.append("\nTesting the hypothesis of agreement using the chi = square test\n\n" + str(n)) #Проверка гипотезы о согласии с помощью критерия хи=квадрат
    
    print("Testing the hypothesis of agreement using the chi = square test:\n") #Проверка гипотезы о согласии с помощью критерия хи=квадрат
    print("Achieved level of significance: " + str(round(pSchi,4))) #Достигнутый уровень значимости
    print("Specified significance level: "+str(alpha)) #Задаваемый уровень значимости
    result = ""
    if pSchi > alpha:
         result = "The hypothesis is not rejected" #Гипотеза не отвергается
    else:
         result = "The hypothesis is rejected" #Гипотеза отвергается
    print(result)
    
    strIntervals = [0]*k
    for i in range(k):
        strIntervals[i] = "[" + str(intervals[i][0]) + ", " + str(intervals[i][1]) + ")"
    tools.drawHist(strIntervals, nin)
    
    content.append("Achieved level of significance: " + str(round(pSchi,4))) #Достигнутый уровень значимости
    content.append("Specified significance level: "+str(alpha)) #Задаваемый уровень значимости
    content.append(result)
    
    workwithFiles.writeToFile("test.txt", content)
