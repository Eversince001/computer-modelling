import generators
import AndersonDarling

def per(N):
    parameters = []
    period = 0
    seq = []

    for i in range(1, 1000):
        
        for j in range(56, 1000):
            print(j)
            for k in range(1000, 10000):
                seq = generators.generateSeq(N, 1, i, j, k)
                seq.reverse()
                period = generators.getPeriod(seq)

                if (period > 100 and AndersonDarling.AndersonDarling(seq, 40, k) > 0.05 and AndersonDarling.AndersonDarling(seq, 40, k) < 1 and AndersonDarling.AndersonDarling(seq, 100, k) > 0.05 and AndersonDarling.AndersonDarling(seq, 100, k) < 1 and AndersonDarling.AndersonDarling(seq, period, k) > 0.05 and AndersonDarling.AndersonDarling(seq, period, k) < 1):
                    parameters.clear()
                    parameters.append(i)
                    parameters.append(j)
                    parameters.append(k)
                    print(period)
                    print(parameters)
                    return parameters



    return parameters