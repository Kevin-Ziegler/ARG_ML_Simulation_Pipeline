#Convert phyformat with ancestral sequence to input required for tsinfer
import tsinfer
import os
import time
import tskit
import sys

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

def reportSolution(fileName, outputDir, length, inferred_ts):
	treesName = fileName + ".trees"
	truepath = dirc + getBaseName(treesName)

	loaded_true = tskit.load(truepath)
	loaded_est = inferred_ts

	t_bp = loaded_true.breakpoints(as_array=True)
	est_bp = loaded_est.breakpoints(as_array=True)


	t_pos = 1
	est_pos = 1
	lastPos = 0
	totalLength = int(length)
	totalWeight = 0 
	totalDist = 0
	flag = 1
	x = []
	y = []

	print(len(t_bp))
	print(len(est_bp))

	while(flag==1):
		weight = 0
		#print(lastPos)
		if( float(t_bp[t_pos]) < float(est_bp[est_pos]) ):
			#print(float(t_bp[t_pos]))
			weight = (float(t_bp[t_pos]) - lastPos)/totalLength
			dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
			lastPos = t_bp[t_pos]
			t_pos+=1
		else:
			#print(float(est_bp[est_pos]))
			weight = (float(est_bp[est_pos]) - lastPos)/totalLength
			dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
			lastPos = est_bp[est_pos]
			est_pos+=1
			if(est_pos == len(est_bp)):
				flag = 0
		


		totalWeight+=weight
		totalDist = totalDist + weight * dist
		#y.append(dist)
		#x.append(lastPos)

	#weight = (totalLength - lastPos)/totalLength
	#dist = loaded_true.at_index(t_pos).kc_distance(loaded_est.at_index(est_pos-2))

	#totalWeight+=weight
	#totalDist = totalDist + weight * dist
	f = open(outputDir + "results", 'a')


	print(totalWeight)
	print(totalDist)
	f.write("FileName: " + fileName+"\n")
	f.write("True Bp: " + 	str(len(t_bp)) + "\n")
	f.write("Est Bp: " + 	str(len(est_bp)) + "\n")
	f.write("KC distance: " + str(totalDist) + "\n")	
	f.close()	



#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/24_2_2020/All/"
#dirc = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/"
#outputDir = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/TsinferOutput/"
#lst_FileNames = ["Standard_Sample_5_Pop_1.0_Recomb_1.0_Rep_0_s_0.00001.phy_m"]
#lst_FileNames = ["Standard_Sample_10_Pop_2.0_Recomb_1.0_Rep_2_s_0.0001.phy_m"]
#length = 100000

dirc = sys.argv[1]
outputDir = sys.argv[2]
lst_FileNames = [sys.argv[3]]
length = sys.argv[4]


#for fileName in os.listdir(dirc):
for fileName in lst_FileNames:
	start = time.time()
	#print(fileName)


	if ".phy_m" in fileName[-6:]:
		#print(float(subRate(fileName)))

		sample_data = tsinfer.SampleData(path=dirc + fileName + "_Tsinfer.samples")


		ancestralseq = ""
		listseqs = []
		listIDs = []
		f = open(dirc + fileName, "r")
		print(dirc+fileName)

		counter = 0
		for line in f:
			if counter == 0:
				x = 1+2
			if counter == 1:
				ancestralseq = line.split()
				ancestralseq = ancestralseq[1]
			if counter > 1:
				listIDs.append(line.split()[0])
				listseqs.append(line.split()[1])
			counter+=1
		f.close()

		#sort sequences so they are in order
		#print(listIDs)
		minID = 0
		indexOfMinID = 0
		for i in range(0, len(listIDs)):
			minID = int(listIDs[i])
			indexOfMinID = i


			for j in range(i, len(listIDs)):
				if int(listIDs[j]) < int(minID):
					minID = int(listIDs[j])
					indexOfMinID = j

			temp = listIDs[i]
			listIDs[i] = listIDs[indexOfMinID]
			listIDs[indexOfMinID] = temp

			temp = listseqs[i]
			listseqs[i] = listseqs[indexOfMinID]
			listseqs[indexOfMinID] = temp


		for i in range(0, len(ancestralseq)):
			ancestralchar = ancestralseq[i]
			allele_lst = [ancestralchar]
			genotypes_lst = []

			for j in range(0,len(listseqs)):

				index = indexOf(listseqs[j][i], allele_lst)
				#print(index)
				if index == -1:
					num = len(allele_lst)
					genotypes_lst.append(num)
					allele_lst.append(listseqs[j][i])
				else:
					genotypes_lst.append(index)
			#print(len(allele_lst))
			if(len(allele_lst) == 2):
				sample_data.add_site(i, genotypes_lst, allele_lst)
				#print("xd")
		sample_data.finalise()
		loaded_data = tsinfer.load(dirc + fileName + "_Tsinfer.samples")
		inferred_ts = tsinfer.infer(loaded_data)
		
		inferred_ts.dump(outputDir + fileName + "_Tsinfer.trees")
		#reportSolution(fileName, outputDir, length, inferred_ts)

