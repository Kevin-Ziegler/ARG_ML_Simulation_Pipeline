import os
import sys

#subrates = [100.0, 10.0, 1.0, 0.0, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/14_2_2020/PopSize/"
dirc = sys.argv[1]
subrates = sys.argv[2]
subrates = subrates.split(",")

nameOfFiles = ".newick"

listOfFiles = os.listdir(dirc)

#subrates = ""
#listOfFiles = ["Standard_Sample_10_Pop_0.0625_Recomb_8.0_Rep_18.newick"]


for i in range(0, len(listOfFiles)):

	if nameOfFiles in listOfFiles[i]:
		f = open(dirc+listOfFiles[i], 'r')
		ancestralSeq = f.readline()
		ancestralSeq = f.readline()

		tailOfFile = listOfFiles[i][:-7]
		print(listOfFiles[i])

		for item in subrates:

			existingPhyFile = tailOfFile + "_s_" + str(item) + ".phy"

			tempFile = []
			f.close()
			print(dirc+existingPhyFile)
			f = open(dirc+existingPhyFile, 'r')
			for line in f:
				tempFile.append(line)

			f.close()

			f = open(dirc+existingPhyFile+"_m", 'w')

			for i in range(0, len(tempFile)):
				if i == 0:
					sline = tempFile[i].split()
					firstline = " " + str(int(sline[0])+1) + " " +sline[1] + "\n"
					secondline = ancestralSeq
					f.write(firstline)
					f.write(secondline)
				else:
					f.write(tempFile[i])
			f.close()

			#os.system("rm " + dirc + existingPhyFile)


