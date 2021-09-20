import workwithFiles
import math

#проверка перестановок
def test1(x, n):
    q = 0
    alpha = 0.05
    u = 1.960

    for i in range(n - 1):
        if x[i] > x[i + 1]:
            q += 1

    leftBorder = q - (u * math.sqrt(n)) / 2
    rightBorder = q + (u * math.sqrt(n)) / 2

    mo = n / 2

    if leftBorder <= mo <= rightBorder:
        resultTest = "Test completed"
        print("Результат теста №1: " + resultTest)
    else:
        resultTest = "Test failed"
        print("Результат теста №1: " + resultTest)

    content = []
    content.append("Test N1\nn=" + str(n) + "\nalpha=0.05\nLevel quantile" + str(
        (1 - alpha / 2)) + "\nQuantile of the standard distribution norm U=" + str(u) +
                   "\nTheoretical mat. waiting M=" + str(mo) + "\nConfidence interval: [" + str(
        leftBorder) + "" + ", " + str(rightBorder) + "]\n" + str(resultTest) + "\n")

    workwithFiles.writeToFile("test.txt", content)
