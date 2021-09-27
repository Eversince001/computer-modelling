import scipy
import math
import workwithFiles
import tools
from scipy import stats

#Частотный тест (тест на равномерность)
def test2(x, n, m, k):
    u = 1.960
    alpha = 0.05
    intervals = [[0] * 2 for i in range(k)] #задаем интервалы
    countInInterval = [0] * k #количество элементов сгенерированной последовательности, попадавших в каждый интервал
    v = [0] * k
    content = []
    leftBorderV = [0] * k
    rightBorderV = [0] * k
    resultTest = ""
    flag = 0

    counter = 0

    for i in range(k):
        intervals[i][0] = counter
        intervals[i][1] = round(m / k + counter, 2)
        counter = intervals[i][1]

        for j in range(n):
            if intervals[i][0] < x[j] < intervals[i][1]:
                countInInterval[i] += 1
        v[i] = countInInterval[i] / n

    strIntervals = [0] * k

    content.append("Test N2\nn=" + str(n))

    for i in range(k):
        strIntervals[i] = "[" + str(intervals[i][0]) + ", " + str(intervals[i][1]) + ")"

    tools.drawHist(strIntervals, v) #Построим гистограмму частот на K отрезках интервала

    resMo = tools.mo(x, n) #Вычислим оценку математического ожидания случайной величины
    resDisp = tools.disp(x, n, resMo) #Вычислим оценку дисперсии случайной величины

    content.append(
        "\nMat. waiting: " + str(resMo) + "\nDisp.: " + str(resDisp) + "\n 1/k = " + str(1 / k))

    for i in range(k):
        leftBorderV[i] = v[i] - (u / k) * math.sqrt((k - 1) / n) #Определяем доверительный интервал для каждой частоты ν
        rightBorderV[i] = v[i] + (u / k) * math.sqrt((k - 1) / n)
        content.append("\nFrequency v" + str(i) + ": " + str(v[i]) + " -> Confidence interval: [" + str(
            leftBorderV[i]) + ", " + str(rightBorderV[i]) + ")\n")

        if not (leftBorderV[i] <= 1 / k <= rightBorderV[i]):
            resultTest = "Test failed"
            content.append(resultTest)
            flag = 1

    theoryMo = m / 2
    theoryDisp = m**2 / 12

    leftBorderMo = resMo - (u * math.sqrt(resDisp)) / math.sqrt(n) #доверительный интервал для МО
    rightBorderMo = resMo + (u * math.sqrt(resDisp)) / math.sqrt(n)

    content.append(
        "\nTheoretical mat. waiting: " + str(theoryMo) + "\nTheoretical disp.: " + str(theoryDisp) + "\n" +
        "Confidence interval of mat. waiting: [" + str(leftBorderMo) + "," + str(rightBorderMo) + ")\n")

    if not (leftBorderMo <= theoryMo <= rightBorderMo):
        #добавить содержимое для файла
        resultTest = "Test failed"
        content.append(resultTest)
        flag = 1
    
    hi0975 = scipy.stats.chi2.ppf(alpha/2, n-1) #Доверительный интервал для дисперии
    hi0025 = scipy.stats.chi2.ppf(1-alpha/2, n-1)


    rightBorderDisp = ((n - 1) * resDisp) / hi0975
    leftBorderDisp = ((n - 1) * resDisp) / hi0025

    content.append("Confidence interval of disp.: [" + str(leftBorderDisp) + "," + str(rightBorderDisp) + ")\n")

    if not (leftBorderDisp <= theoryDisp <= rightBorderDisp):
        resultTest = "Test failed"
        content.append(resultTest)
        flag = 1

    content.append(resultTest)

    if (flag == 0):
        resultTest = "Test completed"
    else:
        resultTest = "Test failed"

    print("Result of test N2: " + resultTest)
    workwithFiles.writeToFile("test.txt", content)

    return resultTest
