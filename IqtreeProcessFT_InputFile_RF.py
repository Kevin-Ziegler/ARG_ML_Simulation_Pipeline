import subprocess
import sys
import os
#import Calc_RF_ETE

def locationSamples(length, numberSamples):
     tempSamples = numberSamples + 1
     stepSize = length/tempSamples
     locationSamples_lst = []

     for i in range(1, tempSamples):
          locationSamples_lst.append(i*stepSize)

     return locationSamples_lst

def extractPos(x):
     num = ""

     for i in range(1, len(x)):
          if x[i] == "]":
               break
          else:
               num = num + x[i]
     return num
def extractNewick(x):
	newick = ""

	flag = 0
	for i in range(0, len(x)):
		if flag == 1:
			newick = newick + x[i]
		if x[i] == "]":
			flag = 1
	return newick[:-1]

def createIqTreeFileName(fileName, subRate, location, windowSize):
	temp = ""
	base = fileName[:-7]
	temp = temp + base + "_s_" + subRate + ".phy_window_" + windowSize + "_locp_" + location + ".iqtree"
	return temp

def getIqTreeNewick(fileName):
	fileN = fileName
	try:
		f = open(fileN, 'r')

		for line in f:
			if "Total time:" in line:
				#f.readline()
				newick = f.readline()
				return newick
		f.close()
	except:
		pass

	return "Consensus Tree or File NotFound"

def findPolyatomy(newick):
	count_comma = 0
	for i in range(0, len(newick)):
		if newick[i]  == "(":
			count_comma = 0
		if newick[i] == ",":
			count_comma +=1
		if newick[i] == ")":
			if count_comma > 1:
				return "Polyatomy"
			count_comma = 0
	return "Not Polyatomy"

def scaleTree(subPerSitePerGen, tree):
	newTree = ""
	flagWriteIt = 0
	tempBranchLength = ""

	for i in range(0, len(tree)):
		if flagWriteIt == 0:
			newTree = newTree + tree[i]

		if tree[i] == ":":
			flagWriteIt = 1
			continue

		if flagWriteIt == 1:

			if tree[i] == "," or tree[i] == ")" or tree[i] == "(":
				temp = float(tempBranchLength) * subPerSitePerGen
				newTree = newTree + str(temp) + tree[i]
				temp = ""
				tempBranchLength = ""
				flagWriteIt = 0
			else:
				tempBranchLength = tempBranchLength + tree[i]

	return newTree

#locationLSD2 = "/pool/Kevin81/Programs/lsd2/bin/"
#dircInputFiles = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/Data/"
#dircIqTreeResults = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/FastTree/"
#windowSizes = [625, 312]
#windowSizes = [10000, 2000, 1000, 500]
#windowSizes = [10000]
#subRates = ["0.0001","0.0000001","0.000000001"]
#subRates = ["0.00000316227"]
#subRates = ["0.0001", "0.00003162277", "0.000000316227"]
#numberSamples = 1
#length = 1000


#locationLSD2 = "/pool/Kevin81/Programs/lsd2/bin/"
dircInputFiles = sys.argv[2]
dircIqTreeResults = sys.argv[3]
windowSizes = sys.argv[4]
windowSizes = windowSizes.split(",")
for i in range(0, len(windowSizes)):
	windowSizes[i] = int(windowSizes[i])
#windowSizes = [10000, 2000, 1000, 500]
#windowSizes = [10000]
subRates = sys.argv[5]
subRates = subRates.split(",")
#for i in range(0,len(subRates)):
#	subRates[i] = float(subRates[i])
#subRates = ["0.00000316227"]
#subRates = ["0.0001", "0.00003162277", "0.000000316227"]
numberSamples = int(sys.argv[6])
length = int(sys.argv[7])
dircCode = sys.argv[8]



locationSamples_lst = locationSamples(length, numberSamples)
print(locationSamples_lst)

inputFileNewick = sys.argv[1]

lstFiles = []

finput = open(inputFileNewick, 'r')
for line in finput:
	lstFiles.append(line[:-1])
finput.close()

outputFile = dircIqTreeResults + "FixedLen_RF_" + inputFileNewick[-2:]




fout = open(outputFile, 'w')



for i in range (0, len(lstFiles)):

	ftemp = open(dircInputFiles + lstFiles[i], 'r')

	ftemp.readline()
	ftemp.readline()
	ftemp.readline()
	position = 0
	oldPos = 0
	maxi = 0
	mini = 0

	for j in range(0, len(locationSamples_lst)):
	#for j in range(0, 4):

		lstTrees = []
		lstOverLap = []
		#print("j: " + str(j))

		if oldPos < (locationSamples_lst[j] - windowSizes[0]): 
			pass
		else:
			ftemp.close()
			ftemp = open(dircInputFiles + lstFiles[i], 'r')

			ftemp.readline()
			ftemp.readline()
			ftemp.readline()

			position = 0
			oldPos = 0
			maxi = 0
			mini = 0

		for k in range(0, len(windowSizes)):


			if k == 0:

				maxi = locationSamples_lst[j] + int(windowSizes[k]/2)
				mini = locationSamples_lst[j] - int(windowSizes[k]/2)
				while(1==1):
					tempOver = 0
					oldPos = position
					if oldPos >= maxi:
						break
					line = ftemp.readline()
					segOfTree = extractPos(line)
					#print(segOfTree)
					#print(oldPos)
					#print(maxi)
					position = position + int(segOfTree)

					if position < mini:
						continue


					if oldPos < mini and position >= mini:
						if position > maxi:
							tempOver = maxi - mini
						else:
							tempOver = position - mini
						lstOverLap.append(tempOver)
						lstTrees.append(extractNewick(line))

					if oldPos > mini:

						if position > maxi:
							tempOver = maxi-oldPos
						else:
							tempOver = position - oldPos
						lstOverLap.append(tempOver)
						lstTrees.append(extractNewick(line))
				#print(lstOverLap)
				#print(lstTrees)

			else:
				#print(k)


				oldMaxi = maxi
				oldMini = mini

				maxi = locationSamples_lst[j] + int(windowSizes[k]/2)
				mini = locationSamples_lst[j] - int(windowSizes[k]/2)

				diff = oldMaxi - maxi

				subLstTrees = []
				subLstOverLap = []

				sumPos = 0
				oldSumPos = 0
				overMaxi = diff + windowSizes[k]

				#print(diff)
				#print(overMaxi)

				for m in range(0, len(lstOverLap)):
					oldSumPos = sumPos
					sumPos = sumPos + lstOverLap[m]

					if sumPos < diff:
						continue
					if oldSumPos > overMaxi:
						break

					if oldSumPos < diff and sumPos >= diff:
						if sumPos > overMaxi:
							tempOver = overMaxi - diff
						else:
							tempOver = sumPos - diff
						subLstOverLap.append(tempOver)
						subLstTrees.append(lstTrees[m])

					if oldSumPos > diff:

						if sumPos > overMaxi:

							tempOver = overMaxi - oldSumPos
						else:	
							tempOver = sumPos - oldSumPos
						subLstOverLap.append(tempOver)
						subLstTrees.append(lstTrees[m])
				#print(subLstOverLap)
				lstTrees = subLstTrees
				lstOverLap = subLstOverLap



			for m in range(0, len(subRates)):
			#for m in range(0,1):
				tempFileName = createIqTreeFileName(dircIqTreeResults + "FT_partition_file_" + lstFiles[i], subRates[m], str(j), str(windowSizes[k]))

				tempFileName = tempFileName[:-7] + ".fastree"

				iqtreeNewick = getIqTreeNewick(tempFileName)
				print(iqtreeNewick)


				if iqtreeNewick == "Consensus Tree or File NotFound":
					fout.write("FileName: " + tempFileName + " \n")
					fout.write("Consensus Tree or File NotFound \n")
					continue


				# poly = findPolyatomy(iqtreeNewick)
				# print(poly)
				# if poly == "Polyatomy":
				# 	print("Polyatomy")
				# 	fout.write("FileName: " + tempFileName + " \n")
				# 	fout.write("Polyatomy \n")
					continue

				print("Length of lstTrees: " + str(len(lstTrees)))
				print(len(lstOverLap))
				print(sum(lstOverLap))
				print(lstOverLap)

				AvgRFDistance = 0
				AvgwRFDistance = 0
				AvgKCDistance = 0
				AvgGRFDistance = 0

				#Convert unrooted iqtree into rooted tree with lsd2

				#create Temp File for isolated consensus iqtree

				# tempfile = open(dircIqTreeResults + lstFiles[i] + "_tempNewickFT", 'w')
				# tempfile.write(iqtreeNewick)
				# tempfile.close()

				# log = subprocess.check_output([locationLSD2 + "lsd2_unix", "-i", dircIqTreeResults + lstFiles[i] + "_tempNewickFT",  "-s",  "10000", "-l", "0", "-r", "a"])
				# #print(dircIqTreeResults + lstFiles[i] + "_tempNewick.result.nwk")
				# rootedTree = subprocess.check_output(["cat", dircIqTreeResults + lstFiles[i] + "_tempNewickFT.result.nwk"])
				# rootedTree = rootedTree.decode('utf-8')
				#print(rootedTree)
				#print(lstTrees[0])

				allNewicksForFile = open(tempFileName + "_allNewick_RF", 'w')
				for n in range(0, len(lstTrees)):
					#s = subprocess.check_output(["Rscript", "KendallColijn2.r", iqtreeNewick, lstTrees[0]])
					#s = subprocess.check_output(["Rscript", "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/KendallColijn2.r"], stderr=subprocess.STDOUT, shell=True)
					#s = subprocess.check_output(["cat /pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/KendallColijn2.r"], stderr=subprocess.STDOUT, shell=True)
					#print(lstTrees[n])
					#tempTree = scaleTree(float(subRates[m]), lstTrees[n])
					allNewicksForFile.write(iqtreeNewick[:-1] + " " + lstTrees[n] + " \n");

					# s = subprocess.check_output(["Rscript", "/pool/Kevin81/LemmonLab/AncestralRecombinationGraphGeneTree/KendallColijn2.r", rootedTree, lstTrees[n]])
					# print(s)
					# s = s.split()
					# s = s[1]
				allNewicksForFile.close()
				#s = subprocess.check_output(["Rscript", dircCode + "RF_File.r", tempFileName + "_allNewick_RF"])
				#print(s)
				#s = s.decode('utf-8')
				#lstRF = Calc_RF_ETE.RF_File(tempFileName + "_allNewick_RF")
				s = subprocess.check_output(["Rscript", dircCode + "Normalize_RemoveSingle_RF.r", tempFileName + "_allNewick_RF"])
				s = s.decode('utf-8')

				lstRF = s.split("\n")
				#bothDistances = s.split("\n")
				#print(bothDistances)
				print(len(lstRF))
				sumw = 0
				for n in range(0, len(lstTrees)):
					temp = lstRF[n]
					distances = temp.split()
					#temp = bothDistances[n]
					#both = temp.split()
					if len(distances) == 0:
						continue
					rf = distances[0]
					wrf = distances[1]
					kc = distances[2]
					grf = distances[3]

					print(n)
					print(rf)
					print(float(lstOverLap[n])/float(windowSizes[k]))
					sumw = sumw + float(lstOverLap[n])/float(windowSizes[k])
					AvgRFDistance = AvgRFDistance + float(lstOverLap[n])/float(windowSizes[k]) * float(rf)
					AvgwRFDistance = AvgwRFDistance + float(lstOverLap[n])/float(windowSizes[k]) * float(wrf)
					AvgKCDistance = AvgKCDistance + float(lstOverLap[n])/float(windowSizes[k]) * float(kc)
					AvgGRFDistance = AvgGRFDistance + float(lstOverLap[n])/float(windowSizes[k]) * float(grf)

				print("Wrote File " + tempFileName)
				print("RF distance is:" + str(AvgRFDistance))
				print(sumw)
				fout.write("FileName: " + tempFileName + " \n")
				fout.write("RF: " + str(AvgRFDistance) + " \n")
				fout.write("wRF: " + str(AvgwRFDistance) + " \n")
				fout.write("KC: " + str(AvgKCDistance) + " \n")
				fout.write("GRF: " + str(AvgGRFDistance) + " \n")
				fout.flush()
			#break
		#break
	#break






	currentLocation = ftemp.readline()	



