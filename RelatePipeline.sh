#!/usr/bin/env bash

#RunPrograms

# dirc=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/
# dircRelate=/home/kevin/Desktop/Research/Programs/relate_v1.0.17_x86_64_dynamic/bin/
# length=99999
# mutationRate=1.25e-8
# popSize=12000
# whichPython=python3
# cmdLineFile=cmdLineRelate
# dircScript=/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/
# dircOutput=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/outputTest2/
# cores=4

DataDirectory=$1
LocationRelate=$2
length=$3
mutationRate=ignore
whichPython=$4
cmdLineFile=relateCmdLine
dircScript=$6
RelateDirectory=$7
cores=$8
ancestralPopSizeUnscaled=$9

program1="${dircScript}CreateRelateCmdLine.py"
program2="${dircScript}RelateRF.py"

echo "number cores"
echo $cores

$whichPython $program1 $DataDirectory $LocationRelate $length $mutationRate $ancestralPopSizeUnscaled $cmdLineFile $whichPython $dircScript $RelateDirectory $cores

temp="Core"

for ((i=1; i<=$cores; i++))
do
 	echo "Welcome $i times"
 	cd $RelateDirectory$temp$i
 	nohup parallel -a $cmdLineFile -j1 > foo.out 2> foo.err < /dev/null &
done
wait




#Process RF distances between results and simulated trees

cmdLineRF="${RelateDirectory}cmdLineRF"
error="${RelateDirectory}RelateRFerror.err"
outfile="${RelateDirectory}RF.out"
errfile="${RelateDirectory}RF.err"

#echo $whichPython $program2 $RelateDirectory $cores $DataDirectory $length $dircScript $whichPython

$whichPython $program2 $RelateDirectory $cores $DataDirectory $length $dircScript $whichPython > $cmdLineRF 2> $error



nohup parallel -a $cmdLineRF -j $cores > $outfile 2> $errfile </dev/null &

wait
