import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
#import more_itertools
#lst = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]
#res = list(more_itertools.flatten(lst))

def flipPopulationSize(x):

	r = len(x)
	c = len(x[0])

	m = np.zeros((r,c))

	for i in range(0, len(x)):

		for j in range(0, len(x[i])):

			m[i][len(x[i])-j-1] = x[i][j]
	return m


#lstFiles = [["/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental2/Results/FastTreeResultsWTE_WRF"]]
#lstNames = ["Reps.pdf", "KC.pdf" , "BP.pdf"]
#titles = ["Number of Replicates", "FastTree 2 RF", "Ratio of BP"]
#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/Tsinfer/AllResults_RF"]]
#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/Tsinfer/AllResults_Reps"]]


#lstFiles =[["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_10k/Tsinfer/AllResults_RF"]]


#lstFiles = [["/pool/Kevin81/NewData_5_31_2023/FastTree/FixedLen_RF_xt_625_RF"]]

#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_16_2020_100k/TsinferSave_1_25_2021/AllResults_RF"]]

#lstFiles = [["/pool/Kevin81/SubSampleLineages/Run2/Results2/Relate_AllResults_RF", "/pool/Kevin81/SubSampleLineages/Run2/Results2/Tsinfer_AllResults_RF", "/pool/Kevin81/SubSampleLineages/Run2/Results2/RentPlus_AllResults_RF"]]

#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/Tsinfer/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/>


#Old Tsinfer Polytomies
#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/Tsinfer/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_10k/Tsinfer/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_16_2020_100k/Tsinfer/AllResults_RF"]]

#Relate
#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/Relate/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_10k/Relate/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_16_2020_100k/Relate/AllResults_RF"]]

#RentPlus
#lstFiles = [["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_1k/RentPlus/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_4_2020_10k/RentPlus/AllResults_RF"], ["/pool/Kevin81/BackUpDrivesPaper/Oct_16_2020_100k/RentPlus/AllResults_RF"]]

#names = ["Tsinfer_1k_Poly.pdf","Tsinfer_10k_Poly.pdf", "Tsinfer_100k_Poly.pdf"]
#names = ["Relate_1k_Poly.pdf","Relate_10k_Poly.pdf", "Relate_100k_Poly.pdf"]
#names = ["RentPlus_1k_Poly.pdf","RentPlus_10k_Poly.pdf", "RentPlus_100k_Poly.pdf"]

#names = ["Tsinfer_1k_Poly_RF60.pdf","Tsinfer_10k_Poly_RF60.pdf", "Tsinfer_100k_Poly_RF60.pdf"]
#names = ["Relate_1k_Poly_RF60.pdf","Relate_10k_Poly_RF60.pdf", "Relate_100k_Poly_RF60.pdf"]
#names = ["RentPlus_1k_Poly_RF60.pdf","RentPlus_10k_Poly_RF60.pdf", "RentPlus_100k_Poly_RF60.pdf"]

#lstFiles = [["/pool/Kevin81/NormalizeWRFTry2/Data/Results/Tsinfer_AllResults_RF"], ["/pool/Kevin81/NormalizeWRFTry2/Data/Results/Tsinfer_AllResults_RF"]]
#names = ["Tsinfer_1k_Subsample.pdf", "Relate_1k_Subsample.pdf"]

lstFiles= [["Tsinfer_AllResults_RF"]]
names = ["Tsinfer WRF"]





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
	print(max_value)

	Mycmap='RdBu_r'
	#fig, axs = plt.subplots(3,1)
	fig, axs = plt.subplots(len(tempLst[0]),len(tempLst))
	min = 0.6703263021006304
	max = 2.2

	mymin = 2.2

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
					elif tempLst[k][j][l][m] < mymin:
						mymin = tempLst[k][j][l][m]

			m = flipPopulationSize(tempLst[k][j])
			#print(m)
			#print(m)
			#print(k)
			sns.heatmap(m, linewidth=0.5, ax=axs[j], vmin=min, vmax=max, cmap='RdBu_r')
			#sns.heatmap(m, linewidth=0.5, ax=axs[j][k], vmin=min, vmax=max, cmap='RdBu_r')
			#axs.set(xlabel='Scaled Population Size', ylabel='Scaled Recombination Rate')
			#plt.title("HeatMap of RF Distance")

	#if i == 0:
	plt.savefig(names[i], dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)

	plt.show()
	print("min")
	print(mymin)

