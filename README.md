Data:

There are 15 Compressed Tar folders in this submission. One folder (DryadPipeLine) contains the code used for this simulation. The remaining folders correspond to datasets:

There are the 10 folders for the 10 replicates used in the main paper (Data1-10.tar.gz)
1 folder representing the distance metrics calculated from each of the 10 replicates 
1 folder of MDS distance matrices and points: AveragedMDS_DistanceMatrix_Points.tar.gz
1 folder simulating a smaller region 10k:Data10k.tar.gz
1 folder simulating a larger region 200k:Data200k.tar.gz


Within Data10k.tar.gz and Data200k.tar.gz, there are 6 directories:
	Data
		-includes mostly simulated data from msprime and seqgen
	Relate
		-files used to run Relate and results
	Tsinfer
		--files used to run Tsinfer and results
	RentPlus
		-files used to run RentPlus and results
	FastTree
		-files used to run FastTree and results
	Results
		-csv like files representing the distance metrics for each method discussed in the mainpaper

The 10 normal replicates used are represented by files  Data1.tar.gz - Data10.tar.gz. These compressed folders contain only the simulated trees and simulated sequences to save space.

Supplemental:
Supplemental Materials.doc contains supplemental Figures



Script Overview:
Code used for simulation, tree estimation, and accuracy comparison (RF, WRF, CID, KC) are provided. (CID distances are represented by files with the tag _GRF. CID is not GRF.)
Code was designed to work on another computer, but this has not been tested. As a result minor errors might need fixing.

Requirements:
Languages used are mainly python, bash for pipelines, and R for RF comparison.
Bash shell scripts will only work in a Linux environment with the parallel command installed.
R packages Required (plus dependencies): ape phangorn TreeDist
Python3 packages: msprime tskit tsinfer
Rent+, Relate, and Seq-gen must be installed separately, and their paths must be specified in the scripts.



Script Files:


There are two bash scripts which are piplines for Co-Estimation methods/Data generation and Maximum Likelihood methods. There is also a general plotting script which needs minor modifications to run on any given file.


1.)
Simulated Data Generation and Co-Estimation methods Can be run with:
./Run_ARG.sh

The script contains variables which need to be set: paths to programs (Seq-gen, Relate, RentPlus), directories (code, data), and simulation parameters.
The pipeline runs subpipelines dealing with, Data generation, Relate, Tsinfer, RentPlus, and then organizing the comparison to simulated trees.
A CSV file representing the heatmap results will be output in the Results/ directory.

The specific scripts and their purpose are listed below:

PipeLine_All.sh
	-Subpipeline used to generate simulated data
testmsprime.py
	-Uses the python package msprime to simulate gene trees for various parameters for a certain number of parameters
SeqGenAncestralNewick.py
	-Creates Newick files with random ancestral sequence for all simulated replicates
createCommandLineToRunSeqGen.py
	-Creates a bash file with all commands to run seq on each replicate
AddAncestralToPhylip.py
	-Adds the ancestral sequence to the simulated output alignments of Seq gen.


RelatePipeline.sh
	-Subpipeline used to run the Co-estimation program Relate
CreateRelateCmdLine.py
	-Create bash script with commands to run Relate for all simulated replicates
Relate_Run.py
	-Runs Relate on all simulated replicates
RelateRF.py
	-Collect Relate outputfiles and creats a bash script with commands to calculate RF distance between simulated and estimated trees
	-Calls Normalize_RemoveSingle_RF.r which calculates tree distance between simulated and estimated trees
RelateConverter_RF2.py
	-calculate RF distance between simulated and estimated trees. Outputs results to a file


TsinferPipeLine.sh
	-Subpipeline used to run the Co-estimation program Tsinfer
CreateTsinferCmdLine.py
	-Create bash script with commands to run Tsinfer for all simulated replicates
TsinferConverter.py
	-Runs Tsinfer on all simulated replicates
TsinferRF.py
	-Collect Tsinfer outputfiles and creats a bash script with commands to calculate RF distance between simulated and estimated trees
TsinferConverter_RF2.py
	-calculate RF distance between simulated and estimated trees. Outputs results to a file


RentPlusPipeLine.sh
	-Subpipeline used to run the Co-estimation program Rent+
CreateRentPlusCmdLine.py
	-Create bash script with commands to run Rent+ for all simulated replicates
RentPlusConverterKZ.py
	-Runs Rent+ on all simulated replicates

RentPlusSolutionPipeLine.sh
	-Subpipeline used to calculate RF distance for Rent+
KendallColijnPrep.py
	-Create subfiles setting up calculation of simulated and estimated trees for Rent+
RentPlus_RF.r
	-calculates tree distance between simulated and estimated trees. Outputs results to a file
CreateResultsRentPlus.py
	-collect result of RF distances and output into a structured file for each replicate.

ResultsToCSV.py
	-Collects output of RF distances for all replicates and converts the data into a single CSV file


2.)
Maximum Likelihood Tree Estimation can be run with:
./Run_ML.sh

The script contains variables which need to be set: paths to programs (FastTree), directories (code, data), and simulation parameters.
A CSV file representing the heatmap results will be output in the Results/ directory.


The specific scripts and their purpose are listed below:
FastTreeWholeEstTrue.py
	-splits simulated alignments in three ways: simulated c-gens, estimated c-gens, and the whole alignment (fixed length 100,000). Runs FastTree on the subsampled alignments and calculates the RF distance between estimated and simulated trees using Rescale_RF_File.r
Normalize_RemoveSingle_RF.r
	-Takes in two newickfiles and calculates RF distance between them
FastTreeResultsWTE.py
	-Collects the RF results file names and put the names in one file
ResultsToCSV_WTE.py
	-Converts the RF results files into a CSV file for plotting

FastTreeScriptCmdLine.py
	-Creates a bash script that runs all other Fixed Lengths on simulated data (312,625,1250,2500,5000,10000) using FastTreeScript.py
FastTreeScript.py
	-Runs FastTree on a given interval Fixed Length intervals
IqtreeProcessFT_InputFile_RF.py
	-Calculates RF distances for Fixed Length estimated trees
Normalize_RemoveSingle_RF.r
	-Takes in two newickfiles and calculates RF distance between them
ResultsToCSV2.py
	-Converts the RF results files into a CSV file for plotting



3.)
A general Plotting script:
PlotHeatMap.py

Line 21 contains the lstFiles variable, which contains the CSV files to plot. 
