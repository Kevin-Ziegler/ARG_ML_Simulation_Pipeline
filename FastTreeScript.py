import os
import subprocess
import sys



baseFileName = sys.argv[1]
windowSize = sys.argv[2]
location = sys.argv[3]
locationIndex = sys.argv[4]
dircAllPartitions = sys.argv[5]
dircInputFiles = sys.argv[6]
dircOutputFiles = sys.argv[7]
locationFastTree = sys.argv[8]


fileNameTemp = "FT_partition_file_" + baseFileName + "_window_" + windowSize + "_locp_" + locationIndex
fileTemp = open(dircAllPartitions + fileNameTemp, 'w')

inputFile = open(dircInputFiles + baseFileName, 'r')
leftIndex = int(float(location) - float(windowSize)/2.0)
rightIndex = int(float(location) + float(windowSize)/2.0)

counter = 0
for line in inputFile:
     if counter == 0 :
          sline = line.split()
          #outputFile.write(" " + sline[0] + " " + str(int(lstRange[1]) - int(lstRange[0])) + " \n")
     else:
          sline = line.split()
          fileTemp.write(">" + sline[0] + " \n" + sline[1][leftIndex:rightIndex] + " \n")
     counter+=1

fileTemp.close()

cmd = locationFastTree + " -nt " + dircAllPartitions + fileNameTemp + " > " + dircOutputFiles + fileNameTemp + ".fastree 2>&1 "
inputF = dircAllPartitions + fileNameTemp
outputF = dircOutputFiles + fileNameTemp +".fastree"
#s = subprocess.check_output(["/pool/Kevin81/Programs/FastTree -nt " + inputF, " > ", outputF, "2>&1"])
try:
     s = subprocess.call([cmd], shell=True)
     print(s)
except subprocess.CalledProcessError as e:
     print("error")
     print(e.output)

