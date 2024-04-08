import subprocess
import tskit
import numpy as np
import sys
import os
#import Calc_RF_ETE

def getBaseName(x):
	count_ = 0
	base = ""

	for item in x:
		if item == "_":
			count_+=1
		if count_ >= 9:
			return base
		else:
			base = base + item
	return base

def subFileFastTree(leftIndex, rightIndex, phyfile, label, OutputDirc, InputDirc, baseFileName):

	fileNameTemp = OutputDirc + "FT_partition_" + label + "_" + phyfile

	fileTemp = open(fileNameTemp, 'w')

	inputFile = open(InputDirc + baseFileName, 'r')

	counter = 0
	for line in inputFile:
	     #print(line)
	     if counter == 0 :
	          sline = line.split()
	     else:
	          sline = line.split()
	          fileTemp.write(">" + sline[0] + " \n" + sline[1][leftIndex:rightIndex] + " \n")
	     counter+=1

	fileTemp.close()
	return fileNameTemp

def subRate(filename):

	count_= 0
	subrate = ""
	for i in range(0, len(filename)):
		if filename[i] == "_":
			count_+=1
			continue
		if count_ == 10:
			subrate = subrate + filename[i]
	return subrate[:-4]

def getFastTreeNewick(fileName):
    fileN = fileName
    try:
            f = open(fileN, 'r')

            for line in f:
                    if "Total time:" in line:
                            #f.readline()
                            newick = f.readline()
                            return newick[:-1]
            f.close()
    except:
            pass

    return "Consensus Tree or File NotFound"
"""
#OLD
def getTotalRFDistance(fileNameNewick, lstWeights, codeDirc):
        flagTsinfer = "0"
        #print(["Rscript", "/pool/Kevin81/LemmonLab/AncestralRecombinationGraphGeneTree/Rescale_RF_File.r", fileNameNewick, flagTsinfer])
        s = subprocess.check_output(["Rscript", codeDirc + "Rescale_RF_File.r", fileNameNewick, flagTsinfer])
        s = s.decode('utf-8')
        #print(s)

        totalRF = 0
        totalWRF = 0


        bothDistances = s.split("\n")
        #print(bothDistances)
        for n in range(0, len(bothDistances)):
                temp = bothDistances[n]
                both = temp.split()
                if len(both) == 0:
                        continue
                rf = both[0]
                wrf = both[1]

                totalRF = totalRF + lstWeights[n] * float(rf)
                totalWRF = totalWRF + lstWeights[n] * float(wrf)

        return [totalRF, totalWRF]
"""

def getTotalRFDistance(fileNameNewick, lstWeights):
	flagTsinfer = "0"
	#print(["Rscript", "/pool/Kevin81/LemmonLab/AncestralRecombinationGraphGeneTree/Rescale_RF_File.r", fileNameNewick, flagTsinfer])
	#s = subprocess.check_output(["Rscript", dircScript + "Rescale_RF_File.r", fileNameNewick, flagTsinfer])
	#s = s.decode('utf-8')
	#lstRF = Calc_RF_ETE.RF_File(fileNameNewick)

	s = subprocess.check_output(["Rscript", codeDirc + "Normalize_RemoveSingle_RF.r", fileNameNewick])
	s = s.decode('utf-8')
	#print(s)

	totalRF = 0
	totalWRF = 0
	totalKC = 0
	totalGRF = 0
	"""print("Finished Computing RF distances")
	if len(lstRF) > 10:
	        print("Ten RF")
	        print(lstRF[:10])
	else:
	        print("Ten RF")
	        print(lstRF)

	print("List Weights")
	if len(lstWeights) > 10:
	        print(lstWeights[:10])
	else:
	        print(lstWeights)
	"""
	lstRF = s.split("\n")
	#print(bothDistances)
	for n in range(0, len(lstRF)):
		temp = lstRF[n]
		distances = temp.split()
		if len(distances) == 0:
			continue
		rf = distances[0]
		wrf = distances[1]
		kc = distances[2]
		grf = distances[3]

		totalRF = totalRF + lstWeights[n] * float(rf)
		totalWRF = totalWRF + lstWeights[n] * float(wrf)
		totalKC = totalKC + lstWeights[n] * float(kc)
		totalGRF = totalGRF + lstWeights[n] * float(grf)

	return [totalRF, totalWRF, totalKC, totalGRF]



def calcRF(loaded_true, loaded_est, t_bp, est_bp, length, ftemp, codeDirc):


	ftempNewick = open(ftemp + "_Newick", 'w')


	t_pos = 1
	est_pos = 1
	lastPos = 0
	totalLength = int(length)
	totalWeight = 0
	totalDist = 0
	flag = 1
	x = []
	y = []
	lstWeight = []

	# print(loaded_true.at_index(0).newick())
	# print(loaded_true.at_index(1).newick())
	# print(loaded_true.at_index(2).newick())
	# print(loaded_true.at_index(3).newick())
	# print(loaded_true.at_index(4).newick())
	# print(loaded_true.at_index(5).newick())


	while(flag==1):
		weight = 0
		#print(lastPos)
		if( float(t_bp[t_pos]) <= float(est_bp[est_pos]) ):
			#print(t_pos)
			#print(est_pos)
			#print(float(t_bp[t_pos]))
			weight = (float(t_bp[t_pos]) - lastPos)/totalLength
			simulatedTree = str(loaded_true.at_index(t_pos-1).newick())
			#simulatedTree = loaded_true[t_pos]
			#estimatedTree = loaded_est.at_index(est_pos-1).newick()
			estimatedTree = str(loaded_est[est_pos-1])
			#estimatedTreeScaled = scaleTree(float(mutationRate), estimatedTree)


			#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))
			tempW = estimatedTree + " " + simulatedTree + " \n"
			ftempNewick.write(tempW)
			ftempNewick.flush()
			lstWeight.append(weight)

			lastPos = t_bp[t_pos]
			t_pos+=1
			if(t_pos > (len(t_bp)-1)):
				print("end true")

				flag = 0
		else:
			#print(t_pos)
			#print(est_pos)
			#print(float(est_bp[est_pos]))
			weight = (float(est_bp[est_pos]) - lastPos)/totalLength
			simulatedTree = str(loaded_true.at_index(t_pos-1).newick())
			#simulatedTree = loaded_true[t_pos]
			#estimatedTree = loaded_est.at_index(est_pos-1).newick()
			estimatedTree = str(loaded_est[est_pos-1])			
			#estimatedTreeScaled = scaleTree(float(mutationRate), estimatedTree)
			tempW = estimatedTree + " " + simulatedTree + " \n"
			ftempNewick.write(tempW)
			ftempNewick.flush()
			lstWeight.append(weight)

			#dist = loaded_true.at_index(t_pos-1).kc_distance(loaded_est.at_index(est_pos-1))

			lastPos = est_bp[est_pos]
			est_pos+=1
			if(est_pos > (len(est_bp)-1)):
				print("end est")
				print(est_pos)
				print((len(est_bp)-1))

				flag = 0




		totalWeight+=weight

	ftempNewick.close()
	totalDist = getTotalRFDistance(ftemp + "_Newick", lstWeight)
	os.remove(ftemp + "_Newick")
	return totalDist


#runFolder = "/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/"
#length = 1000
runFolder = sys.argv[1]
length = sys.argv[2]
codeDirc = sys.argv[3]
locationFastTree = sys.argv[4]
#myFiles = "ListWTEFiles.txt"
myFiles = sys.argv[5]

#runFolder = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Sep_30_2020_1k/"
#runFolder = "/media/alemmon/storage1/Kevin/AncestralRecombinationGraphs/Oct_4_2020_1k/"
#runFolder = sys.argv[1]
#fastTreeDirc = "/pool/Kevin81/Programs/FastTree"
#length = "1000"
#length = sys.argv[2]

#need to make
FastTreeDirc = runFolder + "FastTree/"
FastTreeSubFiles = FastTreeDirc + "SubFiles/"


#s = subprocess.check_output(["mkdir " + FastTreeDirc], shell = True)
#s = subprocess.check_output(["mkdir " + FastTreeSubFiles], shell = True)
#s = subprocess.check_output(["ls " + runFolder  + "Data/ | grep .phy$ > " + runFolder + "LstPhyFiles.txt"], shell = True)



#myFiles = sys.argv[3]



lstAllFileNames = []
fileFileNames = open(runFolder + myFiles, 'r')
for line in fileFileNames:
	lstAllFileNames.append(line[:-1])

for item in lstAllFileNames:
	print(item)
	fileName = item
	treesName = fileName + "_m_Tsinfer.trees"
	estimated = runFolder + "Tsinfer/" + treesName

	truepath = runFolder + "Data/" + getBaseName(fileName)

	loaded_true = tskit.load(truepath)
	try:
		loaded_est = tskit.load(estimated)
		est_bp = loaded_est.breakpoints(as_array=True)
		est_bp = np.append(est_bp, int(length))

	except:
		est_bp = []
	t_bp = loaded_true.breakpoints(as_array=True)

	print("loaded data files")
	#Create Whole Fasta
	fileNameTemp = "FT_partition_whole_" + fileName
	fileTemp = open(FastTreeSubFiles + fileNameTemp, 'w')
	inputFile = open(runFolder + "Data/" + fileName, 'r')

	counter = 0
	for line in inputFile:
	     if counter == 0 :
	          sline = line.split()
	     else:
	          sline = line.split()
	          fileTemp.write(">" + sline[0] + " \n" + sline[1] + " \n")
	     counter+=1

	fileTemp.close()
	wholefn = fileNameTemp

	#Create Estimated Fasta
	lstEstFastTree = []
	lstTrueFastTree = []

	print("created whole fasta")
	print(len(est_bp))
	print(len(t_bp))

	for i in range(1, len(est_bp)):
		if i%1000 == 0:
			print(i)
		start = est_bp[i-1]
		stop = est_bp[i]
		fn = subFileFastTree(int(start), int(stop), fileName, "est_" + str(i), FastTreeSubFiles, runFolder + "Data/", fileName)
		lstEstFastTree.append(fn)



	#Create True Fasta
	# if subRate(fileName) == "0.00000001":
	for i in range(1, len(t_bp)):
		
		if i%1000==0:
			print(i)

		start = t_bp[i-1]
		stop = t_bp[i]
		fn = subFileFastTree(int(start), int(stop), fileName, "t_" + str(i), FastTreeSubFiles, runFolder + "Data/",fileName)
		lstTrueFastTree.append(fn)

	print("Created Fasta Files")

	wholecmd = locationFastTree + " -nt " + FastTreeSubFiles + wholefn + " > " + FastTreeSubFiles + wholefn + ".fastree 2>&1 "

	s = subprocess.check_output([wholecmd], shell=True)
	s = s.decode('utf-8')

	print("Ran whole Tree")

	for i in range(0, len(lstEstFastTree)):
		cmd = locationFastTree + " -nt " + lstEstFastTree[i] + " > " + lstEstFastTree[i] + ".fastree 2>&1 "
		s = subprocess.check_output([cmd], shell=True)
		s = s.decode('utf-8')
	print("Ran Estimated Trees")

	for i in range(0, len(lstTrueFastTree)):
		cmd = locationFastTree + " -nt " + lstTrueFastTree[i] + " > " + lstTrueFastTree[i] + ".fastree 2>&1 "
		s = subprocess.check_output([cmd], shell=True)
		s = s.decode('utf-8')

	print("Ran True Trees")


	lstFastTreeNewickEst = []
	lstFastTreeNewickTrue = []
	lstFastTreeNewickWhole = []


	temp = getFastTreeNewick(FastTreeSubFiles + wholefn + ".fastree")
	lstFastTreeNewickWhole.append(temp)


	for i in range(0, len(lstEstFastTree)):
		temp = getFastTreeNewick(lstEstFastTree[i] + ".fastree")
		lstFastTreeNewickEst.append(temp)

	for i in range(0, len(lstTrueFastTree)):
		temp = getFastTreeNewick(lstTrueFastTree[i] + ".fastree")
		lstFastTreeNewickTrue.append(temp)


	#print("List True then Est BP")
	#print(t_bp)
	#print(est_bp)

	print("Newick from FastTree")
	#print(lstFastTreeNewickEst)
	#print(lstFastTreeNewickTrue)

	wholeRF = calcRF(loaded_true, lstFastTreeNewickWhole, t_bp, [0,int(length)], length, FastTreeSubFiles + fileName + "Whole", codeDirc)
	print(wholeRF)
	if len(est_bp) == 0:
		estRF = ["", "", "", ""]
	else:
		estRF = calcRF(loaded_true, lstFastTreeNewickEst, t_bp, est_bp, length, FastTreeSubFiles + fileName + "Est", codeDirc)
	print(estRF)
	tRF = calcRF(loaded_true, lstFastTreeNewickTrue, t_bp, t_bp, length, FastTreeSubFiles + fileName + "True", codeDirc)
	
	print("Calculated RF Distances")
	print(wholeRF)
	print(estRF)
	print(tRF)

	fout = open(FastTreeDirc + fileName + "_RF_WTE", "w")

	fout.write("wholeRF " + str(wholeRF[0]) + " " + str(wholeRF[1]) + " " + str(wholeRF[2]) + " " + str(wholeRF[3]) + " \n")
	fout.write("EstRF " + str(estRF[0]) + " " + str(estRF[1]) + " " + str(estRF[2]) + " " + str(estRF[3]) + " \n")
	fout.write("TrueRF " + str(tRF[0]) + " " + str(tRF[1]) + " " +str(tRF[2]) + " " +str(tRF[3])  + " \n")

	fout.close()
	
	for item in lstTrueFastTree:
		os.remove(item)
		os.remove(item + ".fastree")
	for item in lstEstFastTree:
		os.remove(item)
		os.remove(item + ".fastree")

	#os.remove(FastTreeSubFiles + fileNameTemp)

