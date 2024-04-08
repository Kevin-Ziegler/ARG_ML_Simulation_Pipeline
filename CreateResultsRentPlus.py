import os
import sys

#totalLength = 100000
#output = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/resultsRentPlus"
#dircInput1 = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCFiles/"
#dircInput2 = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCOutput/"

output = sys.argv[3]
dircInput1 = sys.argv[1]
dircInput2 = sys.argv[2]

lstFiles = []


fout = open(output, 'w')

lstFiles = os.listdir(dircInput2)
counter2 = 0

for item in lstFiles:
	try:
		if "WRF" in item:
			continue

		if counter2%100 == 0:
			print(counter2)
		#print(item)

		input1 = dircInput1 + item
		input2 = dircInput2 + item
		#input3 = dircInput2 + item + "WRF"

		f1 = open(input1, 'r')
		f2 = open(input2, 'r')
		#f3 = open(input3, 'r')
		tempFile = ""
		totalWeight_RF = 0
		totalWeight_WRF = 0
		totalWeight_KC = 0
		totalWeight_GRF = 0
		total_KC = 0
		
		missingWeight = 0
		lastline = ""
		counter = 0
		
		#line2 = f2.readline()
		for line in  f1:
			#print("inloop")
			sline = line.split()
			line2 = f2.readline()
			sline2 = line2.split()
			#line3 = f3.readline()
			#sline3 = line3.split()

			if len(sline2) == 0:
				line2 = f2.readline()
				sline2 = line2.split()

			#if len(sline3) == 0:
			#	line3 = f3.readline()
			#	sline3 = line3.split()


			#print(sline2)
			if (tempFile != sline[3] and counter != 0) or len(sline) == 0:
				#new fileName
				print("in print")
				fout.write("FileName: " + lastline[3] +" \n")
				fout.write("True Bp: " + lastline[4] + " \n")
				fout.write("Est Bp: " + lastline[5] + " \n")
				#fout.write("KC distance: " + str(totalWeight/(1.0-missingWeight)) + " \n")
				fout.write("RF distance: " + str(totalWeight_RF) + " \n")
				fout.write("WRF distance: " + str(totalWeight_WRF) + " \n")
				fout.write("KC distance: " + str(totalWeight_KC) + " \n")
				fout.write("GRF distance: " + str(totalWeight_GRF) + " \n")
				fout.write("BP Ratio: " + str(lastline[6]) + " " + str(lastline[7]) + " \n")

				totalWeight = 0
				total_KC = 0
				missingWeight = 0

				totalWeight_RF = 0
				totalWeight_WRF = 0
				totalWeight_KC = 0
				totalWeight_GRF = 0
			#print(line)
			#print(line2)
			#print(counter)
			if sline2[0] == "NotBinary":
				missingWeight = missingWeight + float(sline[0])
			else:
				totalWeight_RF = totalWeight_RF + float(sline2[0]) * float(sline[0])
				totalWeight_WRF = totalWeight_WRF + float(sline2[1]) * float(sline[0])
				totalWeight_KC = totalWeight_KC + float(sline2[2]) * float(sline[0])
				totalWeight_GRF = totalWeight_GRF + float(sline2[3]) * float(sline[0])
				if float(sline2[0]) * float(sline[0]) < 0:
					print(float(sline2[0]) * float(sline[0]))
					print(line)
					print(line2)

			lastline = sline
			tempFile = sline[3]
			counter+=1
			#line2 = f2.readline()

		fout.write("FileName: " + lastline[3] +" \n")
		fout.write("True Bp: " + lastline[4] + " \n")
		fout.write("Est Bp: " + lastline[5] + " \n")
		#fout.write("KC distance: " + str(totalWeight/(1.0-missingWeight)) + " \n")
		#fout.write("RF distance: " + str(totalWeight) + " \n")
		#fout.write("WRF distance: " + str(totalWeightWRF) + " \n")
		fout.write("RF distance: " + str(totalWeight_RF) + " \n")
		fout.write("WRF distance: " + str(totalWeight_WRF) + " \n")
		fout.write("KC distance: " + str(totalWeight_KC) + " \n")
		fout.write("GRF distance: " + str(totalWeight_GRF) + " \n")
		fout.write("BP Ratio: " + str(lastline[6]) + " " + str(lastline[7]) + " \n")		
		fout.flush()

		f1.close()
		f2.close()
		counter2+=1
	except Exception as e:
		print(e)
		print("Did not work for: " + item)

fout.close()

	# FileName: Standard_Sample_10_Pop_0.5_Recomb_4.0_Rep_1_s_0.00001.phy_m
	# True Bp: 459
	# Est Bp: 2211
	# KC distance: 42.94106094019825

