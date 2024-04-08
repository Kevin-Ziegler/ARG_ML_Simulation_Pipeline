#!/usr/bin/env bash

# Sections/Steps in Pipeline
# directory inputs
# parameter inputs
# make folder data folder
# make output folders
# Create Data
# Run Relate Tsinfer RentPlus
# Get RF distances from each
# create CSV Files
# have to wait accourdinly


#PipeLine To generate data, run programs, and process output into csv files

#Inputs to Modify

#Computer Specific

DirectorySeqGen=/pool/Kevin81/Programs/Seq-Gen-1.3.4/source/
RelateLocation=/pool/Kevin81/Programs/relate/bin/
RentPlusLocation=/pool/Kevin81/Programs/RentPlus/
whichPython="python3"
RentPlusMemUsage="8G"

#Directories
CodeDirectory="/pool/Kevin81/RedoResults_10_12_2023/DryadPipeLine/"
BaseDirectory="/pool/Kevin81/RedoResults_10_12_2023/Data2/"
DataDirectory="${BaseDirectory}Data/"
RelateDirectory="${BaseDirectory}Relate/"
TsinferDirectory="${BaseDirectory}Tsinfer/"
RentPlusDirectory="${BaseDirectory}RentPlus/"
ResultsDirc="${BaseDirectory}Results/"


Simulation Parameters
nameOfFiles=Standard_Sample_10_Pop
lengthofseqs=1000
replicates=1
sampleperpop=10
cores=30
ancestralPopSize=12000

:'
subrates=0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001
recombination_rates=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
scalepopsize=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
'

subrates=0.0001,0.0000001,0.000000001
recombination_rates=8.0,2.0,1.0,0.125
scalepopsize=8.0,1.0,0.125

#Test Parameters
#nameOfFiles=Standard_Sample_10_Pop
#lengthofseqs=1000
#replicates=1
#sampleperpop=10
#cores=4
#ancestralPopSize=12000

#subrates=0.0001,0.0000001,0.000000001
#recombination_rates=8.0,2.0,1.0,0.125
#scalepopsize=8.0,1.0,0.125


#subrates=0.00000001
#recombination_rates=1.0
#scalepopsize=1.0


#Misc
relatecmdLine="{$RelateDirectory}relatecmdLine"


mkdir $BaseDirectory
mkdir $DataDirectory
mkdir $RelateDirectory
mkdir $TsinferDirectory
mkdir $RentPlusDirectory
mkdir $ResultsDirc




#Create Data by calling PipeLine_All.sh 
"${CodeDirectory}PipeLine_All.sh" $CodeDirectory $DataDirectory $DirectorySeqGen $whichPython $nameOfFiles $lengthofseqs $replicates $sampleperpop $cores $subrates $recombination_rates $scalepopsize

wait

echo "done with data"

#Run Relate
echo "Start Relate"
"${CodeDirectory}RelatePipeline.sh" $DataDirectory $RelateLocation $lengthofseqs $whichPython $relatecmdLine $CodeDirectory $RelateDirectory $cores $ancestralPopSize

wait

#RunTSinfer
echo "Start Tsinfer"
"${CodeDirectory}TsinferPipeLine.sh" $DataDirectory $TsinferDirectory $CodeDirectory $lengthofseqs $whichPython $cores

wait

#RunRentPlus
echo "Start RentPlus"
"${CodeDirectory}RentPlusPipeLine.sh" $DataDirectory $RentPlusLocation $RentPlusDirectory $CodeDirectory $whichPython $cores $RentPlusMemUsage $lengthofseqs $ancestralPopSize

#wait


#Convert Results into Csv format
echo "Convert into CSV"
#Relate
find $RelateDirectory -type f | grep result_RF3 | xargs cat > "${RelateDirectory}AllResults"
program3="${CodeDirectory}ResultsToCSV.py"

$whichPython $program3 $subrates $recombination_rates $scalepopsize "${RelateDirectory}AllResults"

#Tsinfer
find $TsinferDirectory -type f | grep result_RF_NP | xargs cat > "${TsinferDirectory}AllResults"
$whichPython $program3 $subrates $recombination_rates $scalepopsize "${TsinferDirectory}AllResults"

#RentPlus
$whichPython $program3 $subrates $recombination_rates $scalepopsize "${RentPlusDirectory}AllResults"
wait


cd $RelateDirectory
ls | grep AllResults_ | xargs -I {} cp {} "../Results/Relate_{}"

cd $TsinferDirectory
ls | grep AllResults_ | xargs -I {} cp {} "../Results/Tsinfer_{}"

cd $RentPlusDirectory
ls | grep AllResults_ | xargs -I {} cp {} "../Results/RentPlus_{}"



