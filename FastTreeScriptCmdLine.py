import os
import subprocess
import sys

def locationSamples(length, numberSamples):
     tempSamples = numberSamples + 1
     stepSize = length/tempSamples
     locationSamples_lst = []

     for i in range(1, tempSamples):
          locationSamples_lst.append(i*stepSize)

     return locationSamples_lst


#length = 1000
#numberSamples = 1
#windowSizes = [625, 312]

#dircAllPartitions = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/SubFiles/"
#dircInputFiles = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/Data/"
#dircOutputFiles = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/"


length = int(sys.argv[1])
numberSamples = int(sys.argv[2])
windowSizes = sys.argv[3]
windowSizes = windowSizes.split(",")
for i in range(0, len(windowSizes)):
	windowSizes[i] = int(windowSizes[i])

dircAllPartitions = sys.argv[4]
dircInputFiles = sys.argv[5]
dircOutputFiles = sys.argv[6]
dircBase = sys.argv[7]
dircCode = sys.argv[8]
locationFastTree = sys.argv[9]

lstFiles = []
cmdLineFastTree = open(dircBase + "cmdLineFastTree", 'w')
locationSamples_lst = locationSamples(length, numberSamples)

lstFilesTemp = os.listdir(dircInputFiles)

for i in range(0, len(lstFilesTemp)):
     if lstFilesTemp[i][-4:] == ".phy":
          lstFiles.append(lstFilesTemp[i])


for i in range(0, len(lstFiles)):


     for j in range(0, len(windowSizes)):

          for k in range(0, len(locationSamples_lst)):

               baseFileName = str(lstFiles[i])
               windowSize = str(windowSizes[j])
               location = str(locationSamples_lst[k])
               locationIndex = str(k)

               
               cmdLine = "python3 " + dircCode + "FastTreeScript.py " + baseFileName + " " + windowSize + " " + location + " " + locationIndex + " " + dircAllPartitions + " " + dircInputFiles + " " + dircOutputFiles + " " + locationFastTree
               cmdLineFastTree.write(cmdLine + " \n")


cmdLineFastTree.close()

