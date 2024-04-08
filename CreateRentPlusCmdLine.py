import os
import sys

dircData = sys.argv[1]
outputDir = sys.argv[2]
whichPython = sys.argv[3]
cmdLineFile = sys.argv[4]
dircScript = sys.argv[5]
dircRentPlus = sys.argv[6]
memUsage = sys.argv[7]


lstFiles = os.listdir(dircData)

#lstFiles = []
#ftemp = open("/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Oct_16_2020_100k/RentPlus/lstNotRun", 'r')
#for line in ftemp:
#	sline = line.split()
#	lstFiles.append(sline[0])
#ftemp.close()

f = open(outputDir + cmdLineFile, 'w')

for i in range(0, len(lstFiles)):
	if(".phy_m" in lstFiles[i][-6:]):
		
		lineToExecute = whichPython + " " + dircScript + "RentPlusConverterKZ.py " + dircData + " " + outputDir + " " + dircRentPlus + " " + lstFiles[i] + " " + memUsage + "\n"
		#print(lineToExecute)
		f.write(lineToExecute)
f.close()
		
