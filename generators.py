
import random

def generateSeq(N, x0, a, c, m):
    seq = []

    seq.append(x0)

    for i in range(N):
        x1 = (a * x0**2 + c) % m
        seq.append(x1)
        x0 = x1

    return seq

def generateSeqPython(N , m):
    seq = [0] * N

    for i in range(N):
        seq[i] = random.randint(0, m)

    return seq

def getPeriod(x):
    period = 0
    for i in range(1, len(x)):
        if(x[0] != x[i]):
            period = period + 1
        else:
            break
        
    return period