import numpy as np
import os
import sys

#subrates="0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001"
#recombination_rates="16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625"
#scalepopsize="16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625"
#resultsdirc = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/FastTree/"

#subrates="0.0001,0.0000001,0.000000001"
#recombination_rates="8.0,2.0,1.0,0.125"
#scalepopsize="8.0,1.0,0.125"

#resultsdirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/RentPlusRF/"

#resultsFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/ResultFiles/June_2_2020_RentPlus_Result_RF"

#resultsdirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/"


#resultsFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/FixedLen_RF_xt"

#windowSizes = ["625", "312"]


subrates=sys.argv[1]
recombination_rates = sys.argv[2]
scalepopsize=sys.argv[3]

resultsdirc = sys.argv[4]
resultsFile = sys.argv[5]

windowSizes = sys.argv[6]
windowSizes = windowSizes.split(",")
#for i in range(0, len(windowSizes)):
#	windowSizes[i] = int(windowSizes[i])

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
lstRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstBP = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstReps = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstWRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
lstGRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))


# lstKC = []
# lstBP = []
# lstReps = []

# for i in range(0, len(subrates)):
# 	temp1a = []
# 	temp2a = []
# 	temp3a = []


# 	for j in range(0, len(recombination_rates)):
# 		temp1 = []
# 		temp2 = []
# 		temp3 = []

# 		for k in range(0, len(scalepopsize)):
# 			temp1.append(0)
# 			temp2.append(0)
# 			temp3.append(0)
# 		temp1a.append(temp1)
# 		temp2a.append(temp2)
# 		temp3a.append(temp3)

# 	lstKC.append(temp1a)
# 	lstBP.append(temp2a)
# 	lstReps.append(temp3a)




# print(lstReps)
# print(lstReps[9,7,6])

#fin = open(resultsFile, 'w')

#lstFiles = os.listdir(resultsdirc)

#for i in range(0, len(lstFiles)):
#	#if("outputFileFT_RF_" in lstFiles[i]) and (("Scaled" in lstFiles[i]) == False):
#	if("outputFileFT_RF_Scaled_" in lstFiles[i]):
#		print(lstFiles[i])
#		ftemp = open(resultsdirc + lstFiles[i], 'r')
#		for line in ftemp:
#			fin.write(line)
#		ftemp.close()
#fin.close()

count_InFastTreePath = 0

for i in range(0, len(resultsdirc)):
	if(resultsdirc[i] == "_"):
		count_InFastTreePath+=1




for itr in range(0, len(windowSizes)):
	print(itr)
	lstRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
	lstWRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
	lstBP = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
	lstReps = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
	lstKC = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))
	lstGRF = np.zeros((len(subrates), len(recombination_rates), len(scalepopsize)))


	f = open(resultsFile, 'r')



	for line in f:
		#print(line)
		sline = line.split()
		#print(sline)
		fileName = sline[1]
		subrate = parseUnderScores(fileName, 13+count_InFastTreePath, 14+count_InFastTreePath)
		subrate = subrate[:-4]
		recombrate = parseUnderScores(fileName, 9+count_InFastTreePath, 10+count_InFastTreePath)
		popSize = parseUnderScores(fileName, 7+count_InFastTreePath, 8+count_InFastTreePath)
		windowSize = parseUnderScores(fileName, 15+count_InFastTreePath, 16+count_InFastTreePath)

		if windowSize == windowSizes[itr]:
			pass
		else:
			line = f.readline()
			line = f.readline()
			line = f.readline()
			line = f.readline()
			continue

		# print(subrate)
		# print(recombrate)
		# print(popSize)

		indexSubrate = indexOf(subrates, subrate)
		indexRecombrate = indexOf(recombination_rates, recombrate)
		indexPopSize = indexOf(scalepopsize, popSize)

		#print(indexSubrate)
		#print(indexRecombrate)
		#print(indexPopSize)

		TrueBp = 0
		EstBp = 0
		RF = 0
		wRF = 0
		KC = 0
		GRF = 0

		#line = f.readline()
		#line = f.readline()
		#line = f.readline()

		line = f.readline()
		sline = line.split()
		if sline[0] == "Consensus":
			continue
		if sline[0] == "Polyatomy":
			continue
		RF = float(sline[1])


		line = f.readline()
		sline = line.split()
		wRF = float(sline[1])

		line = f.readline()
		sline = line.split()
		KC = float(sline[1])

		line = f.readline()
		sline = line.split()
		GRF = float(sline[1])

		#print(RF)
		#print(wRF)
		#print(KC)
		#print(GRF)

		lstReps[indexSubrate, indexRecombrate, indexPopSize] = lstReps[indexSubrate, indexRecombrate, indexPopSize] + 1
		lstRF[indexSubrate,indexRecombrate,indexPopSize] = lstRF[indexSubrate,indexRecombrate,indexPopSize] + RF
		lstWRF[indexSubrate,indexRecombrate,indexPopSize] = lstWRF[indexSubrate,indexRecombrate,indexPopSize] + wRF
		lstKC[indexSubrate,indexRecombrate,indexPopSize] = lstKC[indexSubrate,indexRecombrate,indexPopSize] + KC
		lstGRF[indexSubrate,indexRecombrate,indexPopSize] = lstGRF[indexSubrate,indexRecombrate,indexPopSize] + GRF
		#print(lstReps)
		#print(lstRF)



	f.close()
	#print(lstReps)
	#print(lstRF)

	#break


	foutReps = open(resultsFile + "_" + windowSizes[itr] +"_Reps", 'w')
	foutRF = open(resultsFile + "_" + windowSizes[itr] +"_RF", 'w')
	foutWRF = open(resultsFile + "_" + windowSizes[itr] +"_WRF", 'w')
	foutKC = open(resultsFile + "_" + windowSizes[itr] +"_KC", 'w')
	foutGRF = open(resultsFile + "_" + windowSizes[itr] +"_GRF", 'w')
	#foutBP = open(resultsFile + "_BP", 'w')

	lstFiles = [foutReps, foutRF, foutWRF, foutKC, foutGRF]
	lstLsts = [lstReps, lstRF, lstWRF, lstKC, lstGRF]

	for a in range(0, len(lstFiles)):

		for i in range(0, len(lstLsts[a])):

			for j in range(0, len(lstLsts[a][i])):

				for k in range(0, len(lstLsts[a][i][j])):
					if a != 0:
						if lstReps[i][j][k] != 0:
							lstLsts[a][i][j][k] = lstLsts[a][i][j][k]/lstReps[i][j][k]
					lstFiles[a].write(str(lstLsts[a][i][j][k]))
					if k != (len(lstLsts[a][i][j])-1):
						lstFiles[a].write(",")

				lstFiles[a].write("\n")
			lstFiles[a].write("\n")

		lstFiles[a].close()
