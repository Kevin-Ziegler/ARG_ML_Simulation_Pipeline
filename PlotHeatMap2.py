import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

import os

def flipPopulationSize(x):

	r = len(x)
	c = len(x[0])

	m = np.zeros((r,c))

	for i in range(0, len(x)):

		for j in range(0, len(x[i])):

			m[i][len(x[i])-j-1] = x[i][j]
	return m



#lstFiles= [["Tsinfer_AllResults_RF"]]
#names = ["Tsinfer WRF"]

#dirc = "/pool/Kevin81/NormalizeWRFTry2/Data6/Results/"
dirc = "/pool2/Kevin_ARG_RUN_10_13_2023/Runs/Data1/Results/"
listAllFiles = os.listdir(dirc)

#Endings = ["AllResults_RF", "AllResults_WRF", "AllResults_KC", "AllResults_GRF"]
#Endings_Name = ["ARG_RF", "ARG_WRF", "ARG_KC", "ARG_GRF"]
"""
Endings = ["AllResults_RF", "AllResults_WRF", "AllResults_KC", "AllResults_GRF", ]
Endings_Name = ["ARG_RF", "ARG_WRF", "ARG_KC", "ARG_GRF"]
"""


lstBase = []

lstFiles = []

"""
for item in Endings:
	temp = []
	for item2 in listAllFiles:
		if item in item2:
			temp.append(dirc + item2)
	temp = sorted(temp)
	tempval = temp[1]
	temp[1] = temp[2]
	temp[2] = tempval
	lstFiles.append(temp)

print(lstFiles)
"""


metrics = ["RF", "WRF", "KC", "GRF"]
#Endings = ["FastTree_RF", "FastTree_WRF", "FastTree_KC", "FastTree_GRF",]
#Endings_Name = ["FastTree_RF", "FastTree_WRF", "FastTree_KC", "FastTree_GRF",]
#hardCodedResults = ["FastTreeResultsWTE_T", "FastTreeResultsWTE_E", "FixedLen_RF_All_312_", "FixedLen_RF_All_625_", "FixedLen_RF_All_1250_", "FixedLen_RF_All_2500_", "FixedLen_RF_All_5000_", "FastTreeResultsWTE_W"]

Endings = ["All_RF", "All_WRF", "All_KC", "All_GRF"]
Endings_Name = Endings
hardCodedResults = ["FixedLen_RF_All_312_", "FixedLen_RF_All_625_", "FixedLen_RF_All_1250_", "FixedLen_RF_All_2500_", "FixedLen_RF_All_5000_", "FastTreeResultsWTE_W", "FastTreeResultsWTE_T", "FastTreeResultsWTE_E", "Relate_AllResults_", "Tsinfer_AllResults_", "RentPlus_AllResults_"]
subtitle = ["312", "625", "1250", "2500", "5000", "10000", "T BP", "E BP", "Relate", "Tsinfer", "Rent+"]

for item in metrics:
	temp = []
	for item2 in hardCodedResults:
		temp.append(dirc + item2 + item)
	lstFiles.append(temp)

print(lstFiles)

for i in range(0, len(lstFiles)):

	tempLst = []

	for j in range(0, len(lstFiles[i])):
		#print(i, j)
		f = open(lstFiles[i][j], 'r')

		relate_lst = []
		temp_s = []
		for line in f:
			if line == "\n":

				relate_lst.append(temp_s)
				temp_s = []
				continue

			#print(line)
			sline = line.split(",")
			temp = []
			for k in range(0, len(sline)):
				temp_i = sline[k]
				if temp_i[-1:] == "\n":
					temp_i = temp_i[:-1]
				temp.append(float(temp_i))
			temp_s.append(temp)
		f.close()

		tempLst.append(relate_lst)


	#print(tempLst)
	#print(len(tempLst))
	#print(len(tempLst[0]))
	print("max")
	#res = list(more_itertools.flatten(tempLst))
	#print(max(res))

	n_dim_array = np.array(tempLst)

	max_value = np.max(n_dim_array)
	min_value = np.min(n_dim_array)
	print(max_value)
	print(min_value)

	Mycmap='RdBu_r'
	#fig, axs = plt.subplots(3,1)
	fig, axs = plt.subplots(len(tempLst[0]),len(tempLst))
	fig.set_size_inches(11, 11)
	fig.suptitle(Endings[i])
	cbar_ax = fig.add_axes([.925, .19, .03, .69])
	#min = find_min_max_nested_list(tempLst, find_minimum=True)
	#max = find_min_max_nested_list(tempLst, find_minimum=False)
	min = min_value
	max = max_value
	#mymin = 2.2

	#if wrF set min to 0 max to 2

	if i == 1:
		min = 0
		max = 2.0


	for item in axs:
		print(item)
	for j in range(0, len(tempLst[0])):


		for k in range(0, len(tempLst)):
			#print(k)
			#print(j)

			for l in range(0, len(tempLst[k][j])):

				for m in range(0, len(tempLst[k][j][l])):
					if tempLst[k][j][l][m] == 0:
						tempLst[k][j][l][m] = float("NaN")
						#pass
					#elif tempLst[k][j][l][m] < mymin:
					#	mymin = tempLst[k][j][l][m]

			m = flipPopulationSize(tempLst[k][j])
			#print(m)
			#print(m)
			#print(k)
			#sns.heatmap(m, linewidth=0.5, ax=axs[j], vmin=min, vmax=max, cmap='RdBu_r')
			sns.heatmap(m, linewidth=0.5, ax=axs[j][k], vmin=min, vmax=max, xticklabels=False, yticklabels=False, cmap='RdBu_r', cbar_ax=cbar_ax)
			#axs.set(xlabel='Scaled Population Size', ylabel='Scaled Recombination Rate')
			#plt.title("HeatMap of RF Distance")
			if j == 0:
				atemp = axs[j][k]
				atemp.set_title(subtitle[k])


	#if i == 0:
	#plt.title(Endings[i])
	plt.savefig("Figure" + Endings_Name[i] + ".pdf", dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)

	#plt.show()
	#print("min")
	#print(mymin)

