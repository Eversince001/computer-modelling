

def readFile(file):

    f = open(file, "r")

    list = []

    list.append(float(f.readline()))
    list.append(float(f.readline()))
    list.append(float(f.readline()))

    N = int(f.readline())

    f.close()

    return list, N

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