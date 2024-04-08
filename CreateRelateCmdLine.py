import sys
import os

for item in sys.argv:
	print(item)

dirc = sys.argv[1]
dircRelate = sys.argv[2]
length = sys.argv[3]
mutationRate = sys.argv[4]
popSize = sys.argv[5]
cmdLineFile = sys.argv[6]
whichPython = sys.argv[7]
dircScript = sys.argv[8]
dircOutput = sys.argv[9]
cores = sys.argv[10]

lstFiles = os.listdir(dirc)
lst_LinesToExec = []

for i in range(1, int(cores)+1):
	os.system("mkdir " + dircOutput + "Core" + str(i))
	lst_LinesToExec.append([])

counter = 0
for i in range(0, len(lstFiles)):
	if(".phy_m" in lstFiles[i][-6:]):
		temp = counter % int(cores)
		lineToExecute = whichPython + " " + dircScript + "Relate_Run.py " + dirc + " " + dircRelate + " " + length + " " + mutationRate + " " + popSize + " " + lstFiles[i] + " " + dircOutput + "Core" + str(temp+1) +"/\n"
		lst_LinesToExec[temp].append(lineToExecute)
		counter+=1

for i in range(0, int(cores)):
	f = open(dircOutput + "Core" + str(i+1) + "/" + cmdLineFile, 'w')
	for j in range(0, len(lst_LinesToExec[i])):
		f.write(lst_LinesToExec[i][j])
	f.close()
