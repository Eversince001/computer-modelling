

#чтение входных данных из файла
def readFile(file):
    f = open(file, "r")


    list = [[0] * 3 for i in range(3)]

    for i in range(3):
        list[i][0] = int(f.readline())
        list[i][1] = int(f.readline())
        list[i][2] = int(f.readline())

    f.close()

    return list

def writeToFileSeq(file, seq):
    f = open(file, "a")
    f.seek(0)

    for elem in seq:
        f.write(str(float('{:.3f}'.format(elem))) + "\n")

    f.close()

def writeToFile(file, content):
    f = open(file, "a")
    f.seek(0)

    for elem in content:
        f.write(str((elem)) + "\n")

    f.close()