import sys
import os
import random

#msprimeNewick = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/Standard_Sample_10_Pop_17.0_Recomb_0.015625_Rep_3.newick"
#rentPlus = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/Standard_Sample_10_Pop_17.0_Recomb_0.015625_Rep_3_s_0.0001.phy_m_Rent.haps.trees"
#outputdirc = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCFiles/"
#outputdirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/RentKCFiles/"
#length = "100000"
#dircName = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/"
#dircName = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/April_7_2020/"

outputdirc = sys.argv[1]
length = sys.argv[2]
dircName = sys.argv[3]

print("outputdirc " + outputdirc)
print("length " + length)
print("dircName " + dircName)

def parseMS(x):
	number = ""
	lasti = 0
	for i in range(1, len(x)):
		if(x[i] == "]"):
			lasti = i
			break
		else:
			number = number + x[i]

	return [number, x[lasti+1:-1]]

def parseRentPlus(x):
	x_split = x.split()
	return [x_split[0], x_split[1][:-2]+";"]

def baseFileName(x):
	base = ""
	count_ = 0
	for item in x:
		if item == "_":
			count_+=1
		if count_ == 9:
			break
		base = base + item
	return base

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
		lstEstimated[i] = float(lstEstimated[i])

	for i in range(0, len(lstTrue)):
		lstTrue[i] = float(lstTrue[i]) 

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



lstFiles = os.listdir(dircName)

#Temp Missing Files

#f = open("/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Oct_16_2020_100k/RentPrepFilesmissing.txt", 'r')
#lstFiles = []
#for line in f:
#	lstFiles.append(line[:-1])
#f.close()



#print(len(lstFiles))

countF = 0

for i in range(0, len(lstFiles)):
	tempFile = lstFiles[i]
	#print(tempFile)
	#tempFile = "Standard_Sample_10_Pop_0.0625_Recomb_2.0_Rep_12_s_0.00001.phy_m_Rent.haps.trees"
	if "Rent.haps.trees" in tempFile:
	#if "Standard_Sample_10_Pop_2.0_Recomb_0.0625_Rep_4_s_0.0000001.phy_m_Rent.haps.trees" in tempFile:
	#if "phy_m" in tempFile:
		#tempFile = tempFile + "_Rent.haps.trees"
		print(tempFile)
		countF+=1
		print(countF)
		f2 = open(dircName + tempFile, 'r')
		f = open(dircName + baseFileName(tempFile)+".newick", 'r')
		fout = open(outputdirc + tempFile[:-11]+"_KCPrepFile", 'w')


		t_bp = []
		est_bp = []
		t_bp_trees = []
		est_bp_trees = []

		skip3 = 0
		
		posSimulated = 0
		for line in f:
			
			if skip3 < 3:
				skip3+=1
				continue
			temp = parseMS(line)
			posSimulated = posSimulated + int(temp[0])
			t_bp.append(posSimulated)
			t_bp_trees.append(temp[1])

		for line in f2:
			temp = parseRentPlus(line)
			est_bp.append(temp[0])
			est_bp_trees.append(temp[1])

		f.close()
		f2.close()
		
		#print(tempFile)
		#print(t_bp)
		#print(est_bp)
		if len(est_bp) == 0:
			continue
		#print(t_bp[0])
		#print(est_bp[0])
		#print(t_bp_trees[0])
		#print(est_bp_trees[0])

		t_pos = 0
		est_pos = 0
		lastPos = 0
		totalLength = int(length)
		totalWeight = 0 
		totalDist = 0
		flag = 1
		x = []
		y = []

		t_bp[0] = float(t_bp[0])
		for z in range(1, len(t_bp)):
			t_bp[z] = float(t_bp[z-1]) + float(t_bp[z])
		
		#BP = oneFuncBP(est_bp, t_bp, int(length))
		BPRatio = 1.0
		#BPRatio = BP[0]/BP[1]

		#BP2 = oneFuncBP(t_bp, est_bp, int(length))
		BPRatio2 = 1.0
		#BPRatio2 = BP2[0]/BP2[1]

		while(flag==1):
			#print("inloop")
			weight = 0
			#print(lastPos)
			if( float(t_bp[t_pos]) < float(est_bp[est_pos]) ):
				#print(float(t_bp[t_pos]))
				weight = (float(t_bp[t_pos]) - float(lastPos))/totalLength
				if weight < 0:
					print("true")
					print(str(t_bp[t_pos]))
					print(str(lastPos))
				#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
				fout.write(str(weight) + " " + str(t_bp_trees[t_pos]) + " " + str(est_bp_trees[est_pos])+ " " + tempFile + " " + str(len(t_bp)) + " " + str(len(est_bp)) + " " + str(BPRatio) + " " + str(BPRatio2) + " \n")
				fout.flush()
				lastPos = t_bp[t_pos]
				t_pos+=1
				if(t_pos == len(t_bp)):
					flag = 0
			else:
				#print(float(est_bp[est_pos]))
				weight = (float(est_bp[est_pos]) - float(lastPos))/totalLength
				if weight < 0:
					print("est")
					print(str(est_bp[est_pos]))
					print(str(lastPos))
				#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
				fout.write(str(weight) + " " + str(t_bp_trees[t_pos]) + " " + str(est_bp_trees[est_pos])+ " " + tempFile + " " + str(len(t_bp)) + " " + str(len(est_bp)) + " " + str(BPRatio) + " " + str(BPRatio2) + " \n")
				fout.flush()
				lastPos = est_bp[est_pos]
				est_pos+=1
				if(est_pos == len(est_bp)):
					flag = 0
		
			
		fout.close()
		#break
print(countF)
