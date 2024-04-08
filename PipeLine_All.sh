#!/usr/bin/env bash

echo $#
CodeDirectory=$1
outputdir=$2
dirSeqGen=$3
whichPython=$4

nameOfFiles=$5
lengthofseqs=$6
replicates=$7
sampleperpop=$8
cores=$9

subrates=${10}
recombination_rates=${11}
scalepopsize=${12}

#CodeDirectory=/pool/Kevin81/LemmonLab/AncestralRecombinationGraphGeneTree/
#outputdir=/pool/Kevin81/Data/AncestralRecombinationGraphSimulations/Sep_20_2022_TestSupplemental/
#dirSeqGen=/pool/Kevin81/Programs/Seq-Gen-1.3.4/source/
#whichPython=python3

#nameOfFiles=Standard_Sample_10_Pop
#lengthofseqs=1000
#replicates=1
#sampleperpop=10
#cores=60

#subrates=0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001
#recombination_rates=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
#scalepopsize=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625



program1="${CodeDirectory}testmsprime.py"
program2="${CodeDirectory}SeqGenAncestralNewick.py"
program3="${CodeDirectory}createCommandLineToRunSeqGen.py"
program4="${CodeDirectory}AddAncestralToPhylip.py"

echo $program1
echo $whichPython

echo $outputdir
$whichPython $program1 $outputdir $scalepopsize $recombination_rates $replicates $sampleperpop $lengthofseqs
$whichPython $program2 $outputdir $nameOfFiles $lengthofseqs
$whichPython $program3 $outputdir $subrates $dirSeqGen

cd $dirSeqGen

parallel -a commandlinescript -j$cores > "${outputdir}seqgen.out" 2> "${outputdir}seqgen.err" &
wait


python $program4 $outputdir $subrates

