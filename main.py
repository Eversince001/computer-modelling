import algorithms
import workWithFiles

#inputData[i][0] - N inputData[i][1] - m inputData[i][2] - s
inputData = workWithFiles.readFile("file.txt")
n = inputData[0][0]
m = inputData[0][1]
s = inputData[0][2]
a = []
k = 0

print("Стандартный алгоритм:\n")
N = 1000
x = algorithms.generator(N)

T, x = algorithms.period(x)

if (T < 100):
    print("Invalid data")
    exit()


#задаем раномерную случайную величину
x_40 = []
for i in range(40):
    x_40.append(x[i])

x_100 = []
for i in range(100):
    x_100.append(x[i])

#стандартная
disc_40 = algorithms.discret(x_40, 40, s, n, m)
print(disc_40)
disc_100 = algorithms.discret(x_100, 100, s, n, m)
print(disc_100)
algorithms.hyperg(inputData[0])
algorithms.hyperg(inputData[1])
algorithms.hyperg(inputData[2])

#нестандартная
nestand_dic_40, K = algorithms.nestandart_alg(x_40, 40)
algorithms.teor_puasson(40, 5, K)
print(nestand_dic_40)
nestand_dic_100, K = algorithms.nestandart_alg(x_100, 100)
algorithms.teor_puasson(100, 5, K)
print(nestand_dic_100)
