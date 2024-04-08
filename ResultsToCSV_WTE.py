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

#subrates = sys.argv[1]
#recombination_rates = sys.argv[2]
#scalepopsize = sys.argv[3]

#input_outputFile = sys.argv[4]
#input_outputFile = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_10k/FastTreeResults"
#input_outputFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Oct_16_2020_100k/FastTreeResults"


subrates=sys.argv[1]
recombination_rates=sys.argv[2]
scalepopsize=sys.argv[3]
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


#List going by subrates, recombrate, population scaling rate
lstReps = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstwholeRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstEstRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstTrueRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstwholeWRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstEstWRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstTrueWRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstwholeKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstEstKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstTrueKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

lstwholeGRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstEstGRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstTrueGRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))

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

	wholeRF = 0
	EstRF = 0
	TrueRF = 0

	wholeWRF = 0
	EstWRF = 0
	TrueWRF = 0

	wholeKC = 0
	EstKC = 0
	TrueKC = 0

	wholeGRF = 0
	EstGRF = 0
	TrueGRF = 0


	line = f.readline()
	sline = line.split()
	wholeRF = float(sline[1])
	wholeWRF = float(sline[2])
	wholeKC = float(sline[3])
	wholeGRF = float(sline[4])

	line = f.readline()
	sline = line.split()
	if len(sline) >= 2:
		EstRF = float(sline[1])
		EstWRF = float(sline[2])
		EstKC = float(sline[3])
		EstGRF = float(sline[4])

	line = f.readline()
	sline = line.split()
	TrueRF = float(sline[1])
	TrueWRF = float(sline[2])
	TrueKC = float(sline[3])
	TrueGRF = float(sline[4])

	#print(lstReps)

	lstReps[indexSubrate, indexRecombrate, indexPopSize] = lstReps[indexSubrate, indexRecombrate, indexPopSize] + 1
	lstwholeRF[indexSubrate,indexRecombrate,indexPopSize] = lstwholeRF[indexSubrate,indexRecombrate,indexPopSize] + wholeRF
	lstEstRF[indexSubrate,indexRecombrate,indexPopSize] = lstEstRF[indexSubrate,indexRecombrate,indexPopSize] + EstRF
	lstTrueRF[indexSubrate,indexRecombrate,indexPopSize] = lstTrueRF[indexSubrate,indexRecombrate,indexPopSize] + TrueRF  

	lstwholeWRF[indexSubrate,indexRecombrate,indexPopSize] = lstwholeWRF[indexSubrate,indexRecombrate,indexPopSize] + wholeWRF
	lstEstWRF[indexSubrate,indexRecombrate,indexPopSize] = lstEstWRF[indexSubrate,indexRecombrate,indexPopSize] + EstWRF
	lstTrueWRF[indexSubrate,indexRecombrate,indexPopSize] = lstTrueWRF[indexSubrate,indexRecombrate,indexPopSize] + TrueWRF  


	lstwholeKC[indexSubrate,indexRecombrate,indexPopSize] = lstwholeKC[indexSubrate,indexRecombrate,indexPopSize] + wholeKC
	lstEstKC[indexSubrate,indexRecombrate,indexPopSize] = lstEstKC[indexSubrate,indexRecombrate,indexPopSize] + EstKC
	lstTrueKC[indexSubrate,indexRecombrate,indexPopSize] = lstTrueKC[indexSubrate,indexRecombrate,indexPopSize] + TrueKC  

	lstwholeGRF[indexSubrate,indexRecombrate,indexPopSize] = lstwholeGRF[indexSubrate,indexRecombrate,indexPopSize] + wholeGRF
	lstEstGRF[indexSubrate,indexRecombrate,indexPopSize] = lstEstGRF[indexSubrate,indexRecombrate,indexPopSize] + EstGRF
	lstTrueGRF[indexSubrate,indexRecombrate,indexPopSize] = lstTrueGRF[indexSubrate,indexRecombrate,indexPopSize] + TrueGRF  



f.close()




foutReps = open(input_outputFile + "_Reps", 'w')


foutWRF = open(input_outputFile + "_WRF", 'w')
foutERF = open(input_outputFile + "_ERF", 'w')
foutTRF = open(input_outputFile + "_TRF", 'w')

foutWWRF = open(input_outputFile + "_WWRF", 'w')
foutEWRF = open(input_outputFile + "_EWRF", 'w')
foutTWRF = open(input_outputFile + "_TWRF", 'w')

foutWKC = open(input_outputFile + "_WKC", 'w')
foutEKC = open(input_outputFile + "_EKC", 'w')
foutTKC = open(input_outputFile + "_TKC", 'w')

foutWGRF = open(input_outputFile + "_WGRF", 'w')
foutEGRF = open(input_outputFile + "_EGRF", 'w')
foutTGRF = open(input_outputFile + "_TGRF", 'w')

lstFiles = [foutReps, foutWRF, foutERF, foutTRF, foutWWRF, foutEWRF, foutTWRF, foutWKC, foutEKC, foutTKC, foutWGRF, foutEGRF, foutTGRF]
lstLsts = [lstReps, lstwholeRF, lstEstRF, lstTrueRF, lstwholeWRF, lstEstWRF, lstTrueWRF, lstwholeKC, lstEstKC, lstTrueKC, lstwholeGRF, lstEstGRF, lstTrueGRF]

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



