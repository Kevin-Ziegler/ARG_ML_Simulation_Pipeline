import msprime
import tskit
import sys

outputdir = sys.argv[1]

divTimes = [1300,1600,2000,2600,3300]
popSizes = [5000,5000,5000,5000,5000,12000,12000]

num_replicates = int(sys.argv[4])
samplesize = int(sys.argv[5])
lengthIn = int(sys.argv[6])

#valuesofc = [-2.0,0.0,1.0,2.0,4.0,6.0,8.0,10.0,12.0,14.0,16.0]
valuesofc = sys.argv[2]
valuesofc = valuesofc.split(",")
for i in range(0, len(valuesofc)):
	valuesofc[i] = float(valuesofc[i])

#recombination_rates = [10.0,8.0,6.0,4.0,3.0, 2.0,1.0,0.5,0.25,0.125, 0.0625, 0.03125, 0.015625]
recombination_rates = sys.argv[3]
recombination_rates = recombination_rates.split(",")
for i in range(0, len(recombination_rates)):
	recombination_rates[i] = float(recombination_rates[i])

for reps in range(0, num_replicates):

	for x in range(0, len(valuesofc)):
		c = valuesofc[x]

		popSizes = [5000,5000,5000,5000,5000,12000,12000]


		for i in range(0, len(popSizes)):
			popSizes[i] = popSizes[i]*c

		for recrate in recombination_rates:



			EastAsians = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[0], growth_rate = 0)
			NorthAsians = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[1], growth_rate = 0)
			Europeans = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[2], growth_rate = 0)
			Oceanians = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[3], growth_rate = 0)
			EastAfricans = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[4], growth_rate = 0)
			WestAfricans = msprime.PopulationConfiguration(sample_size=samplesize, initial_size = popSizes[5], growth_rate = 0)

			m = 0.0
			d = 6
			#migration_matrix = [[0, m, m],[m, 0, m], [m, m, 0]]

			migration_matrix = []
			temp = []
			for i in range(0, d):
				temp.append(m)
				
			for i in range(0,d):
				temp2 = temp.copy()
				temp2[i] = 0
				migration_matrix.append(temp2)

			#print(migration_matrix)



			population_configurations = [WestAfricans, EastAfricans, Oceanians, Europeans, NorthAsians, EastAsians]

			EastAsianNorthAsianMerge = msprime.MassMigration(time = divTimes[0], source = 5, dest = 4, proportion = 1.0)
			EastAsianNorthAsianPopUpdate = msprime.PopulationParametersChange(time = divTimes[0], initial_size = popSizes[1], growth_rate = 0, population_id = 4)
			EastAsianNorthAsianPopUpdate2 = msprime.PopulationParametersChange(time = divTimes[0], initial_size = 1, growth_rate = 0, population_id = 5)
			x1 = msprime.MigrationRateChange(time=divTimes[0], rate=0)

			NorthAsianEuropeanMerge = msprime.MassMigration(time = divTimes[1], source = 4, dest = 3, proportion = 1.0)
			NorthAsianEuropeanPopUpdate = msprime.PopulationParametersChange(time = divTimes[1], initial_size = popSizes[2], growth_rate = 0, population_id = 3)
			NorthAsianEuropeanPopUpdate2 = msprime.PopulationParametersChange(time = divTimes[1], initial_size = 1, growth_rate = 0, population_id = 4)
			x2 = msprime.MigrationRateChange(time=divTimes[1], rate=0)

			EuropeanOceanianMerge = msprime.MassMigration(time = divTimes[2], source = 3, dest = 2, proportion = 1.0)
			EuropeanOceanianPopUpdate = msprime.PopulationParametersChange(time = divTimes[2], initial_size = popSizes[3], growth_rate = 0, population_id = 2)
			EuropeanOceanianPopUpdate2 = msprime.PopulationParametersChange(time = divTimes[2], initial_size = 1, growth_rate = 0, population_id = 3)
			x3 = msprime.MigrationRateChange(time=divTimes[2], rate=0)

			OceanianEastAfricanMerge = msprime.MassMigration(time = divTimes[3], source = 2, dest = 1, proportion = 1.0)
			OceanianEastAfricanPopUpdate = msprime.PopulationParametersChange(time = divTimes[3], initial_size = popSizes[4], growth_rate = 0, population_id = 1)
			OceanianEastAfricanPopUpdate2 = msprime.PopulationParametersChange(time = divTimes[3], initial_size = 1, growth_rate = 0, population_id = 2)
			x4 = msprime.MigrationRateChange(time=divTimes[3], rate=0)

			EastAfricanWestAfricanMerge = msprime.MassMigration(time = divTimes[4], source = 1, dest = 0, proportion = 1.0)
			EastAfricanWestAfricanPopUpdate = msprime.PopulationParametersChange(time = divTimes[4], initial_size = popSizes[5], growth_rate = 0, population_id = 0)
			EastAfricanWestAfricanPopUpdate2 = msprime.PopulationParametersChange(time = divTimes[4], initial_size = 1, growth_rate = 0, population_id = 1)
			x5 = msprime.MigrationRateChange(time=divTimes[4], rate=0)


			demography = [EastAsianNorthAsianMerge, x1, EastAsianNorthAsianPopUpdate, EastAsianNorthAsianPopUpdate2,
						NorthAsianEuropeanMerge, x2, NorthAsianEuropeanPopUpdate, NorthAsianEuropeanPopUpdate2,
						EuropeanOceanianMerge, x3, EuropeanOceanianPopUpdate, EuropeanOceanianPopUpdate2,
						OceanianEastAfricanMerge, x4, OceanianEastAfricanPopUpdate, OceanianEastAfricanPopUpdate2,
						EastAfricanWestAfricanMerge, x5, EastAfricanWestAfricanPopUpdate, EastAfricanWestAfricanPopUpdate2]


			#tree_sequence = msprime.simulate(length=5e3, recombination_rate=2e-8, mutation_rate=2e-8, random_seed=10, num_replicates = 2, population_configurations = population_configurations)
			tree_sequence = msprime.simulate(length=lengthIn, recombination_rate = (1e-8)*recrate, population_configurations = population_configurations, migration_matrix = migration_matrix, demographic_events = demography)
			#dd = msprime.DemographyDebugger(population_configurations = population_configurations, migration_matrix = migration_matrix, demographic_events = demography)
			"""
			print(tree_sequence)

			for item in tree_sequence:
				tree = item.first()
				print(tree.draw(format="unicode"))
			"""

			#temp = tree_sequence[0]
			#for tree in tree_sequence.trees():
			#	print("-" * 20)
			#	print("tree {}: interval = {}".format(tree.index, tree.interval))
			#	print(tree.draw(format="unicode"))
			#	print(tree.newick())

			# x = tree_sequence.breakpoints()

			#for item in x:
			#	print(item)


			tree_sequence.dump(outputdir + "Standard_Sample_10_Pop_" + str(c)+"_Recomb_" + str(recrate) + "_Rep_"+str(reps))


			#y = tskit.load("/pool/Kevin/LemmonLab/AncestralRecombinationGraphGeneTree/file1")
			#x = y.breakpoints()

