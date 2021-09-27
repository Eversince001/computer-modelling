import test1
import test2
import workwithFiles

#Проверка подпоследовательностей на случайность и равномерность
def test3(x, n, m, r, k):
    t = round((n - 1) / r)
    pp = [0] * t
    flag = 0

    for i in range(r): #генерация r последовательностей
        for j in range(t):
            pp[j] = x[j * r + i]

        print(pp)
        if test1.test1(pp, len(pp)) == "Test failed":
            flag = 1
            break

        if test2.test2(pp, len(pp), m, k) == "Test failed":
            flag = 1
            break

    if flag == 0:
        resultTest = "Test completed"
    else:
        resultTest = "Test failed"

    content = []
    content.append("Test N3\nn=" + str(n) + "\n" + str(resultTest))

    workwithFiles.writeToFile("test.txt", content)
