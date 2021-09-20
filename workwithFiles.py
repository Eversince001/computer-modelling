

#чтение входных данных из файла
def readFile(file):
    f = open(file, "r")

    list = []
    list.append(int(f.readline())) #a
    list.append(int(f.readline())) #c
    list.append(int(f.readline())) #m
    list.append(int(f.readline())) #N
    list.append(int(f.readline())) #x0
    list.append(int(f.readline())) #K - test2
    list.append(int(f.readline())) #r
    list.append(int(f.readline())) #K - test3

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