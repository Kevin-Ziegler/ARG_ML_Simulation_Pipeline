import os
import sys

#dirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/"
#dirc = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Oct_16_2020_100k/FastTree/"
#dirc = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_1k/FastTree/"
#dirc = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_10k/FastTree/"
dirc = sys.argv[1]



lstFiles = os.listdir(dirc)

outputFile = dirc + "FastTreeResultsWTE"
#outputFile = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_1k/FastTreeResults"
#outputFile = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_10k/FastTreeResults" 

f = open(outputFile, 'w')

for i in range(0, len(lstFiles)):
	if "phy_RF_WTE" in lstFiles[i]:
		lines = []
		ftemp = open(dirc + lstFiles[i], 'r')
		for line in ftemp:
			lines.append(line)
		ftemp.close()

		f.write("FileName: " + lstFiles[i] + " \n")
		for item in lines:
			f.write(item)
f.close()
