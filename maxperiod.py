import generators

def per(N):
    parameters = []
    period = 0
    seq = []

    for i in range(10, 1000):
        
        for j in range(10, 1000):

            for k in range(100, 700):
                seq = generators.generateSeq(N, 1, i, j, k)
                seq.reverse()
                period = generators.getPeriod(seq)

                if (period > 100):
                    parameters.clear()
                    parameters.append(i)
                    parameters.append(j)
                    parameters.append(k)
                    print(period)
                    print(parameters)
                    break



    return parameters