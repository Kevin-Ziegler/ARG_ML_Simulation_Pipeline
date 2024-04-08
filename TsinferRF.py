#$TsinferDirectory $DataDirectory $cores $length $CodeDirectory > $cmdLineRF

#length = sys.argv[5]
#mutationRate = sys.argv[4]
#popSize = "12000"
#inputFile = sys.argv[1]
#outputDir = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/June_2_2020_Relate/TreeFiles/"
#outputDir = "/pool/Kevin81/Data/AncestralRecombinationGraphSimul



import os
import subprocess
import sys
import TestSplit

tsinferDir = sys.argv[1]
cores = sys.argv[3]
dirSimulated = sys.argv[2]
length = sys.argv[4]
dirScript = sys.argv[5]
whichPython = sys.argv[6]

line2 = "ls " + tsinferDir + " | grep .trees$ > " + tsinferDir + "ListTreeFiles.txt"
x2 = subprocess.check_output([line2], shell=True)

line3 = "wc -l " + tsinferDir + "ListTreeFiles.txt"
x3 = subprocess.check_output([line3], shell=True)

#print("Lines", x3)

splitx3 = x3.split()

#print("Heck", splitx3)
linesPerCore = str(int(int(splitx3[0])/int(cores) + 1))

#line4 = "split -l " + linesPerCore + " --numeric-suffixes " + tsinferDir + "ListTreeFiles.txt ListTreeFiles"
#print(line4)
#x4 = subprocess.check_output([line4], shell=True)
#x4 = subprocess.check_output(["split -l ", linesPerCore, " --numeric-suffixes ", tsinferDir, "ListTreeFiles.txt", "ListTreeFiles"], shell=True)

TestSplit.split_file(tsinferDir + "ListTreeFiles.txt", tsinferDir + "ListTreeFiles", int(cores))


for i in range(0, int(cores)):
	if i <= 9:
		file = tsinferDir + "ListTreeFiles0" + str(i)
	else:
		file = tsinferDir + "ListTreeFiles" + str(i)

	print(whichPython + " " + dirScript + "RelateConverter_RF2.py " + file + " " + tsinferDir + " " + tsinferDir + "result_RF_NP_" + str(i) + " " + dirSimulated + " " + length + " " + dirScript)


