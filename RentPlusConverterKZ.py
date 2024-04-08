import os
from collections import Counter
import sys

# dircData = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/"
# fileName = "Standard_Sample_10_Pop_2.0_Recomb_1.0_Rep_4_s_0.00001.phy_m"
# dircRentPlus = "/home/kevin/Desktop/Research/Programs/RentPlus/"


dircData = sys.argv[1]
dircOutput = sys.argv[2]
dircRentPlus = sys.argv[3]
fileName = sys.argv[4]
memUsage = sys.argv[5]

def indexOf(x, lst):
        for i in range(0, len(lst)):
                if x == lst[i]:
                        return i
        return -1



outputF = open(dircData + str(fileName) + "_Rent.haps", "w")

listRent = []



if ".phy_m" in fileName[-6:]:



	ancestralseq = ""
	listseqs = []
	listIDs = []
	f = open(dircData + fileName, "r")
	print(dircData+fileName)

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

	for i in range(0, len(listIDs)):
		listRent.append("")
	listRent.append("")

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
			#line = "1 . " + str(i) + " " + str(allele_lst[0]) + " " + str(allele_lst[1])
			
			listRent[0] = listRent[0] + str(i) + " "
			for z in range(0, len(genotypes_lst)):
				#line = line + " " + str(item)
				listRent[z+1] = listRent[z+1] + str(genotypes_lst[z])
			#print("wrote line")
			#outputF.write(line+"\n")
	for i in range(0, len(listRent)):
		#print(listRent[i])
		outputF.write(listRent[i] + " \n")
outputF.close()



#Run Rent
print("Trying to Run Rent")
lineToExecute = "java -Xmx" + memUsage + " -jar " + dircRentPlus + "RentPlus.jar -t " + dircData + str(fileName) + "_Rent.haps "
print(lineToExecute)
os.system(lineToExecute)
