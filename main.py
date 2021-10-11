import generators
import workwithFiles
import test1
import test2
import test3
import X
import AndersonDarling
import maxperiod

inputData = workwithFiles.readFile("file.txt")

#inputData[0] - a, inputData[1] - c, inputData[2] - m
#inputData[3] - N, inputData[4] - x0, inputData[5] - K для теста №2
#inputData[6] - r, inputData[7] - K для теста №3 

#tmp  = maxperiod.per(inputData[3])

#print(tmp)

seq = generators.generateSeq(inputData[3], inputData[4], inputData[0], inputData[1], inputData[2])
#seq = generators.generateSeqPython(inputData[3], inputData[2])

workwithFiles.writeToFileSeq("seqFile.txt", seq)


reverseSeq = seq.copy()
reverseSeq.reverse()
period = generators.getPeriod(reverseSeq)

print("Период = " + period.__str__())

#test1.test1(reverseSeq, 40)
#test1.test1(reverseSeq, 100)

#test2.test2(reverseSeq, 40, inputData[2], inputData[5])
#test2.test2(reverseSeq, 100, inputData[2], inputData[5])

#test3.test3(reverseSeq, 40, inputData[2], inputData[6], inputData[7])
#test3.test3(reverseSeq, 100, inputData[2], inputData[6], inputData[7])

#X.X(reverseSeq, 40, inputData[5])
#X.X(reverseSeq, 100, inputData[5])
#X.X(reverseSeq, period, inputData[5])

AndersonDarling.AndersonDarling(reverseSeq, 40, inputData[2])
AndersonDarling.AndersonDarling(reverseSeq, 100, inputData[2])
AndersonDarling.AndersonDarling(reverseSeq, period, inputData[2])