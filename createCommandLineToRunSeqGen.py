import os
import sys

#dirc = "/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/Data/14_2_2020/PopSize/"
#subrates = [100.0, 10.0, 1.0, 0.0, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]



dirc = sys.argv[1]
subrates = sys.argv[2]
dircSeqGen = sys.argv[3]

subrates = subrates.split(",")

print(subrates)

nameOfFiles = ".newick"
#outputdirc = "/home/alemmon/Downloads/Seq-Gen-master/source/"
outputdirc = dircSeqGen

listOfFiles = os.listdir(dirc)
tempfilepath = outputdirc+"commandlinescript"
print(tempfilepath)
f = open(tempfilepath, 'w')

counter = 1
for i in range(0, len(listOfFiles)):
	#print(listOfFiles[i])

	if nameOfFiles in listOfFiles[i]:
		tempf = open(dirc+listOfFiles[i], 'r')
		numPartitions = tempf.readline()
		numPartitions = tempf.readline()
		numPartitions = tempf.readline()
		#strip newline character
		numPartitions = numPartitions[:-1]

		for item in subrates:
			seqgenCommand = "./seq-gen -mHKY -t0.5 -fe -z" + str(counter) + " -p" + numPartitions + " -s" + str(item)+" -k1 < " + dirc + listOfFiles[i]+ " > " + dirc + listOfFiles[i][:-7]+"_s_"+str(item) + ".phy"
			#seqgenCommand = "./seq-gen -mHKY -t0.5 -fe -p" + numPartitions + " -s" + str(item)+" -k1 < " + dirc + listOfFiles[i]+ " > " + dirc + listOfFiles[i][:-7]+"_s_"+str(item) + ".phy"
			#print(seqgenCommand)
			f.write(seqgenCommand + "\n")
			counter+=1

f.close()
