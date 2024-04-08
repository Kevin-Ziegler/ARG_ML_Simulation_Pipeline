import os
import sys

dircData = sys.argv[1]
outputDir = sys.argv[2]
length = sys.argv[3]
whichPython = sys.argv[4]
cmdLineFile = sys.argv[5]
dircScript = sys.argv[6]


lstFiles = os.listdir(dircData)
f = open(outputDir + cmdLineFile, 'w')

for i in range(0, len(lstFiles)):
	if(".phy_m" in lstFiles[i][-6:]):
		
		lineToExecute = whichPython + " " + dircScript + "TsinferConverter.py " + dircData + " " + outputDir + " " + lstFiles[i] + " " + length + "\n"
		#print(lineToExecute)
		f.write(lineToExecute)
f.close()
		
