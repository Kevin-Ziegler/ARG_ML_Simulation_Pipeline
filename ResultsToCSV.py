import numpy as np
import sys


#subrates="0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001"
#recombination_rates="16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625"
#scalepopsize="16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625"

#subrates="0.00000001"
#recombination_rates="1.0"
#scalepopsize="1.0"

#resultsFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/ResultFiles/Sep_3_2020_200k_Tsinfer"
#resultsFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/ResultFiles/June_2_2020_Tsinfer_RF"

subrates = sys.argv[1]
recombination_rates = sys.argv[2]
scalepopsize = sys.argv[3]

input_outputFile = sys.argv[4]


subrates=subrates.split(",")
recombination_rates=recombination_rates.split(",")
scalepopsize=scalepopsize.split(",")


print(subrates)

def indexOf(lst, x):
	for i in range(0, len(lst)):

		#print(lst[i])
		#print(x)
		if lst[i] == x:
			return i
	return -1

def parseUnderScores(x, begin, end):
	count_ = 0
	temp = ""

	for i in range(0, len(x)):
		if x[i] == "_":
			count_+=1
			if count_ == end:
				break
		else:
			if count_ >= begin and count_ < end:
				temp = temp + x[i]
	return temp 


#dist1 = RF dist2 WRF dist3 KC dist4 Generalized RF
#List going by subrates, recombrate, population scaling rate
#lstKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstBP = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstReps = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstDist1 = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstDist2 = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstDist3 = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstDist4 = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstBPRatio = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstBPRatioT = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstBPTrue = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstBPEst = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))


# print(lstReps)
# print(lstReps[9,7,6])


f = open(input_outputFile, 'r')

for line in f:

	#print(line)
	sline = line.split()
	#print(sline)

	fileName = sline[1]
	subrate = parseUnderScores(fileName, 10, 11)
	subrate = subrate[:-4]
	recombrate = parseUnderScores(fileName, 6, 7)
	popSize = parseUnderScores(fileName, 4, 5)

	# print(subrate)
	# print(recombrate)
	# print(popSize)

	indexSubrate = indexOf(subrates, subrate)
	indexRecombrate = indexOf(recombination_rates, recombrate)
	indexPopSize = indexOf(scalepopsize, popSize)

	# print(indexSubrate)
	# print(indexRecombrate)
	# print(indexPopSize)

	TrueBp = 0
	EstBp = 0
	KC = 0


	line = f.readline()
	sline = line.split()
	TrueBp = float(sline[2])


	line = f.readline()
	sline = line.split()
	EstBp = float(sline[2])

	line = f.readline()
	sline = line.split()
	RF = float(sline[2])

	line = f.readline()
	sline = line.split()
	WRF = float(sline[2])

	line = f.readline()
	sline = line.split()
	KC = float(sline[2])

	line = f.readline()
	sline = line.split()
	GRF = float(sline[2])

	line = f.readline()
	sline = line.split()
	bpRatio = float(sline[2])
	bpRatioT = float(sline[3])

	#print(lstReps)

	lstReps[indexSubrate, indexRecombrate, indexPopSize] = lstReps[indexSubrate, indexRecombrate, indexPopSize] + 1
	#lstKC[indexSubrate,indexRecombrate,indexPopSize] = lstKC[indexSubrate,indexRecombrate,indexPopSize] + KC

	lstDist1[indexSubrate,indexRecombrate,indexPopSize] = lstDist1[indexSubrate,indexRecombrate,indexPopSize] + RF
	lstDist2[indexSubrate,indexRecombrate,indexPopSize] = lstDist2[indexSubrate,indexRecombrate,indexPopSize] + WRF
	lstDist3[indexSubrate,indexRecombrate,indexPopSize] = lstDist3[indexSubrate,indexRecombrate,indexPopSize] + KC
	lstDist4[indexSubrate,indexRecombrate,indexPopSize] = lstDist4[indexSubrate,indexRecombrate,indexPopSize] + GRF

	lstBPRatio[indexSubrate,indexRecombrate,indexPopSize] = lstBPRatio[indexSubrate,indexRecombrate,indexPopSize] + bpRatio
	lstBPRatioT[indexSubrate,indexRecombrate,indexPopSize] = lstBPRatioT[indexSubrate,indexRecombrate,indexPopSize] + bpRatioT
	
	lstBPTrue[indexSubrate,indexRecombrate,indexPopSize] = lstBPTrue[indexSubrate,indexRecombrate,indexPopSize] + TrueBp
	lstBPEst[indexSubrate,indexRecombrate,indexPopSize] = lstBPEst[indexSubrate,indexRecombrate,indexPopSize] + EstBp

	if TrueBp > EstBp:
		lstBP[indexSubrate,indexRecombrate,indexPopSize] = lstBP[indexSubrate,indexRecombrate,indexPopSize] + (EstBp-TrueBp)/TrueBp
	else:
		lstBP[indexSubrate,indexRecombrate,indexPopSize] = lstBP[indexSubrate,indexRecombrate,indexPopSize] + (EstBp-TrueBp)/EstBp




f.close()




foutReps = open(input_outputFile + "_Reps", 'w')


#foutKC = open(input_outputFile + "_RF", 'w')
foutBP = open(input_outputFile + "_BP", 'w')

foutDist1 = open(input_outputFile + "_RF", 'w')
foutDist2 = open(input_outputFile + "_WRF", 'w')
foutDist3 = open(input_outputFile + "_KC", 'w')
foutDist4 = open(input_outputFile + "_GRF", 'w')

foutBPRatio = open(input_outputFile + "_BPRatio", 'w')
foutBPRatioT = open(input_outputFile + "_BPRatioT", 'w')
foutBPTrue = open(input_outputFile + "_BPTrue", 'w')
foutBPEst = open(input_outputFile + "_BPEst", 'w')

lstFiles = [foutReps, foutDist1, foutDist2, foutDist3, foutDist4, foutBP, foutBPRatio, foutBPRatioT, foutBPTrue, foutBPEst]
lstLsts = [lstReps, lstDist1, lstDist2, lstDist3, lstDist4, lstBP, lstBPRatio, lstBPRatioT, lstBPTrue, lstBPEst]

for itr in range(0, len(lstFiles)):

	for i in range(0, len(lstLsts[itr])):

		for j in range(0, len(lstLsts[itr][i])):

			for k in range(0, len(lstLsts[itr][i][j])):
				if itr != 0:
					if lstReps[i][j][k] != 0:
						lstLsts[itr][i][j][k] = lstLsts[itr][i][j][k]/lstReps[i][j][k]
				lstFiles[itr].write(str(lstLsts[itr][i][j][k]))
				if k != (len(lstLsts[itr][i][j])-1):
					lstFiles[itr].write(",")

			lstFiles[itr].write("\n")
		lstFiles[itr].write("\n")

	lstFiles[itr].close()



