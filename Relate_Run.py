#Convert phyformat with ancestral sequence to input required for tsinfer
import os
import time
import tskit
import sys

#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/24_2_2020/All/"
#dircRelate = "~/Downloads/relate_v1.0.17_x86_64_dynamic/bin/"

#dirc = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_7_2020/"
#dircRelate = "/home/kevin/Desktop/Research/Programs/relate_v1.0.17_x86_64_dynamic/bin/"
#length = "99999"
#mutationRate = "1.25e-8"
#popSize = "12000"


dirc = sys.argv[1]
dircRelate = sys.argv[2]
length = sys.argv[3]
#mutationRate = sys.argv[4]
popSize = sys.argv[5]
inputFile = sys.argv[6]
outputDir = sys.argv[7]

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
		




recombParam = -99
lst_RunTimes = []
#lst_FileNames = os.listdir(dirc)
lst_FileNames = [inputFile]

#for fileName in os.listdir(dirc):
for fileName in lst_FileNames:
	start = time.time()
	print(fileName)


	if ".phy_m" in fileName[-6:]:
		mutationRate = subRate(fileName)
		recombParam = getRecombParam(fileName)
		popParam = getPopParam(fileName)
		popSize = float(popSize) * popParam
		popSize = str(popSize)
		

		outputF = open(dirc + fileName + "_Relate.haps", 'w')


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



		#print(listIDs)
		#print(ancestralseq)
		#print(listseqs)
		genotypes_lst = []
		#print(len(listseqs))

		for i in range(0, len(ancestralseq)):
			ancestralchar = ancestralseq[i]
			allele_lst = [ancestralchar]
			genotypes_lst = []

			for j in range(0,len(listseqs)):

				#if ((j+1)% 5) == 0:
				#	continue


				index = indexOf(listseqs[j][i], allele_lst)
				#print(index)
				if index == -1:
					num = len(allele_lst)
					genotypes_lst.append(num)
					allele_lst.append(listseqs[j][i])
				else:
					genotypes_lst.append(index)
			#print(len(genotypes_lst))
			#print(len(allele_lst))
			if(len(allele_lst) == 2):
				#sample_data.add_site(i, genotypes_lst, allele_lst)
				#print("xd")
				line = "1 . " + str(i) + " " + str(allele_lst[0]) + " " + str(allele_lst[1])
				for item in genotypes_lst:
					line = line + " " + str(item)
				#print("wrote line")
				outputF.write(line+"\n")

		outputF.close()


		fsamples = open(dirc + fileName + ".samples", 'w')
		fsamples.write("ID_1 ID_2 missing\n0    0    0\n")
		for i in range(0, int(len(genotypes_lst)/2)):
			fsamples.write("0    0    0\n")
		fsamples.close()

		fgeneticmap = open(dirc+ fileName + "_geneticmap.txt", 'w')
		fgeneticmap.write("pos COMBINED_rate Genetic_Map\n")
		recomb_cm_mb = CM_MB(recombParam)
		recomb_dist = genetic_Pos(recomb_cm_mb)

		fgeneticmap.write("0\t" + str(recomb_cm_mb) + "\t0\n")
		fgeneticmap.write(length + "\t0\t" + str(recomb_dist) +"\n")
		fgeneticmap.close()


		#lineToExecute = " ~/Downloads/relate_v1.0.17_x86_64_dynamic/bin/Relate --haps " + dirc + fileName + "_Relate.haps  --sample " + dirc + fileName + ".samples --mode All -m " + mutationRate + " -N " + popSize + " --map " + dirc + fileName + "_geneticmap.txt --seed 1 -o " + fileName
		lineToExecute = dircRelate + "Relate --haps " + dirc + fileName + "_Relate.haps  --sample " + dirc + fileName + ".samples --mode All -m " + mutationRate + " -N " + popSize + " --map " + dirc + fileName + "_geneticmap.txt --seed 1 -o " + fileName

		os.system(lineToExecute)

		#PATH_TO_RELATE/bin/RelateFileFormats --mode ConvertToTreeSequence -i example -o example
		#lineToExecute2 = "~/Downloads/relate_v1.0.17_x86_64_dynamic/bin/RelateFileFormats --mode ConvertToTreeSequence -i " + fileName + " -o " + fileName
		lineToExecute2 = dircRelate + "RelateFileFormats --mode ConvertToTreeSequence -i " + fileName + " -o " + fileName
		print(lineToExecute2)
		os.system(lineToExecute2)

		
