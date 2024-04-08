#!/usr/bin/env bash

DataDirectory=$1
RentPlusLocation=$2
RentPlusDirectory=$3
CodeDirectory=$4

whichPython=$5
cmdLineFile=cmdLineRentPlus
cores=$6
memUsage=$7
length=$8
popSize=$9



Script1="CreateRentPlusCmdLine.py"
Script1L=$CodeDirectory$Script1



echo $Script1L
$whichPython $Script1L $DataDirectory $RentPlusDirectory $whichPython $cmdLineFile $CodeDirectory $RentPlusLocation $memUsage

cd $RentPlusDirectory

outF=rentP.out
outE=rentP.err
outFF=$outputDir$outF
outEE=$outputDir$outE

nohup parallel -a $cmdLineFile -j $cores > $outFF 2> $outEE < /dev/null &

wait

#Get RF between estimated trees and simulated trees 
echo "Before RF"
echo $CodeDirectory
what=$CodeDirectory

echo "All Params"

echo $whichpython
echo $RentPlusDirectory
echo $length
echo $DataDirectory
echo $cores
echo $CodeDirectory
echo $what


"${CodeDirectory}RentPlusSolutionPipeLine.sh" $whichPython $RentPlusDirectory $length $DataDirectory $cores $CodeDirectory $popSize $what

wait
