import algorithms
import workWithFiles


#inputData[i][0] - N inputData[i][1] - m inputData[i][2] - n
inputData = workWithFiles.readFile("file.txt")

#Для стандартного алгоритма при N = 20, m = 10, n = 4
print("Стандартный алгоритмЖ:\n")
seq40 = algorithms.builtInGenerator(40)
print(seq40)
workWithFiles.writeToFileSeq("firstfile", seq40)

SEQ40 = algorithms.HypergeometricDistribution(40, inputData[0], seq40)

#Для стандартного алгоритма при N = 20, m = 10, n = 10

#Для стандартного алгоритма при N = 30, m = 15, n = 10