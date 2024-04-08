#Convert phyformat with ancestral sequence to input required for tsinfer
#Version 2 uses newick files
import os
import time
import tskit
import sys
import subprocess
import random
#import Calc_RF_ETE
import numpy as np

#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/24_2_2020/All/"
#dircRelate = "~/Downloads/relate_v1.0.17_x86_64_dynamic/bin/"

#dirc = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_7_2020/"
#dircRelate = "/home/kevin/Desktop/Research/Programs/relate_v1.0.17_x86_64_dynamic/bin/"
#length = "99999"
#mutationRate = "1.25e-8"
#popSize = "12000"



#dirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/August_10_2020_100k/"
#dircRelate = "/pool/Kevin81/Programs/relate_v1.0.17_x86_64_dynamic/bin/"
#length = "99999"
length = sys.argv[5]
#mutationRate = sys.argv[4]
popSize = "12000"
inputFile = sys.argv[1]
#outputDir = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020_Relate/TreeFiles/"
#outputDir = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020_Tsinfer_Output/"
outputDir = sys.argv[2]
outputFile = sys.argv[3]
#outputFile = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020_Tsinfer/resultRF"
dirc = sys.argv[4]
dircScript = sys.argv[6]

def indexOf(x, lst):
	for i in range(0, len(lst)):
		if x == lst[i]:
			return i
	return -1

def subRate(filename):

	count_= 0
	subrate = ""
	for i in range(0, len(filename)):
		if filename[i] == "_":
			count_+=1
			continue
		if count_ == 10:
			subrate = subrate + filename[i]
	return subrate[:-4]


def CM_MB(rec_base_gen):
	return (1-(1-rec_base_gen*1*10**-8)**1000000)*100

def genetic_Pos(CM_MB):
	return (CM_MB*99999.0)/(1e6*1.0)

def getRecombParam(x):
	count_ = 0
	rec = ""
	for item in x:

		if item == "_":
			count_ +=1
			continue
		if count_ == 6:
			rec = rec + item
	return float(rec)

def getPopParam(x):
	count_ = 0
	pop = ""
	for item in x:

		if item == "_":
			count_ +=1
			continue
		if count_ == 4:
			pop = pop + item
	return float(pop)


def getBaseName(x):
	count_ = 0
	base = ""

	for item in x:
		if item == "_":
			count_+=1
		if count_ >= 9:
			return base
		else:
			base = base + item
	return base


def getTotalRFDistance(fileNameNewick, lstWeights):
	flagTsinfer = "0"
	#print(["Rscript", "/pool/Kevin81/LemmonLab/AncestralRecombinationGraphGeneTree/Rescale_RF_File.r", fileNameNewick, flagTsinfer])
	s = subprocess.check_output(["Rscript", dircScript + "Normalize_RemoveSingle_RF.r", fileNameNewick, flagTsinfer])
	s = s.decode('utf-8')
	#lstRF = Calc_RF_ETE.RF_File(fileNameNewick)
	#print(lstRF)

	#print(s)

	totalRF = 0
	totalWRF = 0
	totalKC = 0
	totalGRF = 0
	"""print("Finished Computing RF distances")
	if len(lstRF) > 10:
		print("Ten RF")
		print(lstRF[:10])
	else:
		print("Ten RF")
		print(lstRF)

	print("List Weights")
	if len(lstWeights) > 10:
		print(lstWeights[:10])
	else:
		print(lstWeights)
	"""
	lstRF = s.split("\n")
	#print(bothDistances)
	for n in range(0, len(lstRF)):
		temp = lstRF[n]
		distances = temp.split()
		#print(distances)
		if len(distances) < 3:
			continue
		rf = distances[0]
		wrf = distances[1]
		kc = distances[2]
		grf = distances[3]

		totalRF = totalRF + lstWeights[n] * float(rf)
		totalWRF = totalWRF + lstWeights[n] * float(wrf)
		totalKC = totalKC + lstWeights[n] * float(kc)
		totalGRF = totalGRF + lstWeights[n] * float(grf)

	return [totalRF, totalWRF, totalKC, totalGRF]



def scaleTree(subPerSitePerGen, tree):
	newTree = ""
	flagWriteIt = 0
	tempBranchLength = ""

	for i in range(0, len(tree)):
		if flagWriteIt == 0:
			newTree = newTree + tree[i]

		if tree[i] == ":":
			flagWriteIt = 1
			continue

		if flagWriteIt == 1:

			if tree[i] == "," or tree[i] == ")" or tree[i] == "(":
				temp = float(tempBranchLength) * subPerSitePerGen
				newTree = newTree + str(temp) + tree[i]
				temp = ""
				tempBranchLength = ""
				flagWriteIt = 0
			else:
				tempBranchLength = tempBranchLength + tree[i]

	return newTree
		
def simulatedTreesFromNewick(fileName):

	trees = []
	bp = []
	
	f = open(fileName, 'r')

	f.readline()
	f.readline()
	f.readline()
	totalLength = 0

	for line in f:

		tempLength = ""
		tempTree = ""
		flagLength = 0
		for i in range(1, len(line)):
			if line[i] == "]":
				flagLength = 1
				continue
			if flagLength == 0:
				tempLength = tempLength + line[i]
			else:
				tempTree = tempTree + line[i]

		totalLength = totalLength + float(tempLength)		
		trees.append(tempTree)
		bp.append(totalLength)

	return [bp, trees]

def createRandomSortedList(num, start, end): 
    arr = [] 
    tmp = random.randint(start, end) 
      
    for x in range(num): 
          
        while tmp in arr: 
            tmp = random.randint(start, end) 
              
        arr.append(tmp) 
          
    arr.sort() 
      
    return arr 

def BPDiff(lstTrue, lstEstimated):
	indexTrue = 0
	sumEstDist = 0

	for i in range(0, len(lstEstimated)):
		#print(i)
		estDist = "a"

		while ((indexTrue != (len(lstTrue)-1)) and (lstTrue[indexTrue+1] <= lstEstimated[i])):
			#print("in while")
			indexTrue+=1
			if (indexTrue) == (len(lstTrue)-1):
				break
		#print("Index true: " + str(indexTrue))

		if (indexTrue) == (len(lstTrue)-1):
			estDist = abs(lstTrue[indexTrue] - lstEstimated[i])
		else:
			#print("not last")
			if abs(lstTrue[indexTrue] - lstEstimated[i]) < abs(lstTrue[indexTrue+1] - lstEstimated[i]):
				estDist = abs(lstTrue[indexTrue] - lstEstimated[i])
			else:
				estDist = abs(lstTrue[indexTrue+1] - lstEstimated[i])

		sumEstDist = sumEstDist + estDist

	return sumEstDist/len(lstEstimated)

def probAverage(x, totallength):

	sumprob = 0
	for i in range(0, len(x)):

		if i == 0:
			sumprob = sumprob + x[i]/totallength * x[i]/2.0
		else:
			sumprob = sumprob + (x[i]-prevlength)/totallength * (x[i]-prevlength)/2.0
		prevlength = x[i]

	
	sumprob = sumprob + (totallength-x[len(x)-1])/totallength * (totallength-x[len(x)-1])/2.0

	return sumprob

def oneFuncBP(lstEstimated, lstTrue,lengthseq):

	estDiff = BPDiff(lstTrue, lstEstimated)

	avgR = 0
	for i in range(0, 100):
		lstRandom = createRandomSortedList(len(lstEstimated), 0, lengthseq)
		randomDiff = BPDiff(lstTrue, lstRandom)
		#print(randomDiff)
		avgR = avgR + randomDiff
	avgR = avgR/100.0

	return [estDiff, avgR]




recombParam = -99
lst_RunTimes = []
#lst_FileNames = os.listdir(dirc)
#lst_FileNames = [inputFile]

lst_FileNames = []
fin = open(inputFile, 'r')
for line in fin:
	lst_FileNames.append(line)
fin.close()


f = open(outputFile, 'w')
#f = open("/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020_Relate/results_RF_" + inputFile[-3:], 'w')


#for fileName in os.listdir(dirc):
for fileName in lst_FileNames:
	start = time.time()
	print(fileName)


	if ".phy_m" in fileName:

		fileName = fileName[:-7]

		mutationRate = subRate(fileName)
		recombParam = getRecombParam(fileName)
		popParam = getPopParam(fileName)
		popSize = float(popSize) * popParam
		popSize = str(popSize)
		


		ancestralseq = ""
		listseqs = []
		listIDs = []
		#f = open(dirc + fileName, "r")
		#print(dirc+fileName)

		
		#try:
		treesName = fileName + ".trees"
		estimated = outputDir + treesName
		truepath = dirc + getBaseName(treesName)

		truepathnewick = truepath + ".newick"

		#print(estimated)
		#print(truepath)

		both = simulatedTreesFromNewick(truepathnewick)

		#loaded_true = tskit.load(truepath)
		loaded_est = tskit.load(estimated)


		ftempNewick = open(estimated + "_Newick", 'w')
		lstWeight = []


		#t_bp = loaded_true.breakpoints(as_array=True)
		est_bp = loaded_est.breakpoints(as_array=True)
		t_bp = both[0]
		loaded_true = both[1]
		#est_bp = np.append(est_bp, int(length))
		#print("BreakPoints")
		#print(t_bp)
		#print(est_bp)

		t_pos = 0
		est_pos = 1
		lastPos = 0
		#totalLength = int(length)
		totalWeight = 0 
		totalDist = 0
		flag = 1
		x = []
		y = []

		#print(len(t_bp))
		#print(len(est_bp))
		#print(t_bp[len(t_bp)-1])
		#print(est_bp[len(est_bp)-1])
		#print(est_bp[0])
		#Change length to be the estimated length! This is weird. Tsinfer seems to have 1 less tree than breakpoints... 
		totalLength = float(est_bp[len(est_bp)-1]) - float(est_bp[0])

		#print(loaded_est.at_index(0).newick())
		#print(loaded_est.at_index(1).newick())

		while(flag==1):
			weight = 0
			#print(lastPos)
			#print("True Pos:", t_pos)
			#print("Est Pos:", est_pos)

			if( float(t_bp[t_pos]) < float(est_bp[est_pos]) ):
				#print(float(t_bp[t_pos]))
				weight = (float(t_bp[t_pos]) - lastPos)/totalLength
				#simulatedTree = loaded_true.at_index(t_pos-1).newick()
				simulatedTree = loaded_true[t_pos]
				estimatedTree = loaded_est.at_index(est_pos-1).newick()

				#estimatedTreeScaled = scaleTree(float(mutationRate), estimatedTree)


				#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
				ftempNewick.write(estimatedTree + " " + simulatedTree + " \n")
				ftempNewick.flush()
				lstWeight.append(weight)

				lastPos = float(t_bp[t_pos])
				t_pos+=1
				if(t_pos > (len(t_bp)-1)):
					flag = 0
			else:
				#print(float(est_bp[est_pos]))
				weight = (float(est_bp[est_pos]) - lastPos)/totalLength
				#simulatedTree = loaded_true.at_index(t_pos-1).newick()
				simulatedTree = loaded_true[t_pos]
				estimatedTree = loaded_est.at_index(est_pos-1).newick()
				#estimatedTreeScaled = scaleTree(float(mutationRate), estimatedTree)

				ftempNewick.write(estimatedTree + " " + simulatedTree + " \n")
				ftempNewick.flush()
				lstWeight.append(weight)

				#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))

				lastPos = float(est_bp[est_pos])
				est_pos+=1
				if(est_pos > (len(est_bp)-1)):
					flag = 0
			


			totalWeight+=weight

		ftempNewick.close()
		

		totalDist = getTotalRFDistance(estimated + "_Newick", lstWeight)
		#Calc_RF_ETE.RF_File(estimated + "_Newick", lstWeight)

		BP = oneFuncBP(est_bp, t_bp, int(length))
		BPRatio = BP[0]/BP[1]

		BP2 = oneFuncBP(t_bp, est_bp, int(length))
		BPRatio2 = BP2[0]/BP2[1]



		#totalDist = totalDist + weight * dist
		#y.append(dist)
		#x.append(lastPos)

		#weight = (totalLength - lastPos)/totalLength
		#dist = loaded_true.at_index(t_pos).kc_distance(loaded_est.at_index(est_pos-2))

		#totalWeight+=weight
		#totalDist = totalDist + weight * dist

		#print(totalWeight)
		#print(totalDist)
		f.write("FileName: " + fileName + " \n")
		f.write("True Bp: " + 	str(len(t_bp)) + " \n")
		f.write("Est Bp: " + 	str(len(est_bp)) + " \n")
		f.write("RF distance: " + str(totalDist[0]) + " \n")	
		f.write("WRF distance: " + str(totalDist[1]) + " \n")
		f.write("KC distance: " + str(totalDist[2]) + " \n")
		f.write("GRF distance: " + str(totalDist[3]) + " \n")
		f.write("BP Ratio: " + str(BPRatio) + " " + str(BPRatio2) + " \n")
		f.flush()

		#os.remove(estimated + "_Newick")

f.close()	



