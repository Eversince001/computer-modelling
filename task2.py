
def FileReadWrite(fileName):
    f = open(fileName, "r+")
    tmp = f.read()
    print('\n' + tmp + '\n')
    f.write('\n' + tmp + '\n')
    f.close()