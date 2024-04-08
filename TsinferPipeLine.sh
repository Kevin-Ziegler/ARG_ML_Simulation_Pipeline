#!/usr/bin/env bash

#dircData=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/
#outputDir=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/TsinferOutput/
#dircScript=/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/

DataDirectory=$1
TsinferDirectory=$2
CodeDirectory=$3

length=$4
whichPython=$5
cores=$6
cmdLineFile=cmdLineTsinfer

program1="${CodeDirectory}CreateTsinferCmdLine.py"
program2="${CodeDirectory}TsinferRF.py"

$whichPython $program1 $DataDirectory $TsinferDirectory $length $whichPython $cmdLineFile $CodeDirectory

cd $TsinferDirectory
nohup parallel -a $cmdLineFile -j $cores > foo.out 2> foo.err < /dev/null &

wait


#Calculate RF distance between simulated and estimated trees


cmdLineRF="${TsinferDirectory}cmdLineRF"
RFout="${TsinferDirectory}RF.out"
RFerr="${TsinferDirectory}RF.err"
$whichPython $program2 $TsinferDirectory $DataDirectory $cores $length $CodeDirectory $whichPython > $cmdLineRF

nohup parallel -a $cmdLineRF -j $cores > $RFout 2> $RFerr &

wait


