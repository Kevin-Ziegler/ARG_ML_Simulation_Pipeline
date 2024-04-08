import os
import tskit
import random
import sys


def createRandomSequenceJC(length):
	seq = ""
	for i in range(0, length):
		temp = random.randint(1,4)
		if(temp == 1):
			seq = seq + "A"
		if(temp == 2):
			seq = seq + "T"
		if temp == 3:
			seq = seq + "G"
		if temp == 4:
			seq = seq + "C"
	return seq



#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/14_2_2020/PopSize/"
#nameOfFiles = "Standard_Sample_5_Pop"
#lengthofseqs = "100000"

dirc = sys.argv[1]
nameOfFiles = sys.argv[2]
lengthofseqs = sys.argv[3]
listOfFiles = os.listdir(dirc)

#dirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020/"
#nameOfFiles = "Standard_Sample_10_Pop"
#lengthofseqs = "100000"
#listOfFiles = ["Standard_Sample_10_Pop_0.0625_Recomb_8.0_Rep_18"]

for i in range(0, len(listOfFiles)):
	#print(listOfFiles[i])
	if ".newick" in listOfFiles[i] or ".phy" in listOfFiles[i]:
		continue

	if nameOfFiles in listOfFiles[i]:
		tree_seq = tskit.load(dirc+listOfFiles[i])
		#print("w")

		f = open(dirc+listOfFiles[i]+".newick", 'w')
		bp = tree_seq.breakpoints()
		listbp = []
		for item in bp:
			listbp.append(item)
		ancseq = createRandomSequenceJC(int(lengthofseqs))
		f.write("1 " + lengthofseqs+"\n")
		f.write("AncestralSeq " + ancseq+"\n")
		f.write(str(len(listbp)-1)+"\n")

		counter = 0
		for tree in tree_seq.trees():
			nw = tree.newick()
			#nw = "((raccoon:19.19959,bear:6.80041):0.84600,((sea_lion:11.99700, seal:12.00300):7.52973,((monkey:100.85930,cat:47.14069):20.59201, weasel:18.87953):2.09460):3.87382,dog:25.46154);"
			f.write("[" + str(round(listbp[counter+1]) - round(listbp[counter]))+"]" + nw+"\n")
			counter+=1
		f.close()
