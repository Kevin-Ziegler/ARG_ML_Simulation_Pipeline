#!/usr/bin/env bash

dircOutput="/pool/Kevin81/BackUpDrivesPaper/June_2_2020/"
length="100000"
codeDirc="/pool/Kevin81/DryadPipeLine/"
cores=30
numberSubSamples=10
windowSizes=10000,5000,2500,1250,625,312
#subrates=0.0001,0.0000001,0.000000001
#recombination_rates=8.0,2.0,1.0,0.125
#scalepopsize=8.0,1.0,0.125

subrates=0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001
recombination_rates=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
scalepopsize=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625


LocationFastTree="/pool/Kevin81/BackUpDriveCode_2018_2021/Programs/FastTree"



#FastTreeDirc="${dircOutput}FastTree/"
#FastTreeSubFiles="${FastTreeDirc}SubFiles/"
#ResultsDirc="${dircOutput}Results/"

FastTreeDirc="/pool/Kevin81/BackUpDrivesPaper/FastTreeResults/FastTree/Results/"
FastTreeSubFiles="/pool/Kevin81/BackUpDrivesPaper/FastTreeResults/FastTree/SubFiles/"
ResultsDirc="/pool/Kevin81/RedoRF_FixedLen/"



mkdir $FastTreeDirc
mkdir $FastTreeSubFiles
mkdir $ResultsDirc

#Data="${dircOutput}Data/"
Data=$dircOutput

#cd $Data

#ls | grep .phy$ > ../ListWTEFiles.txt


#Run ML with Estimated and True Breakpoints along with the whole length
#python3 "${codeDirc}FastTreeWholeEstTrue.py" $dircOutput $length $codeDirc $LocationFastTree
wait

#python3 "${codeDirc}FastTreeResultsWTE.py" $FastTreeDirc
wait

#python3 "${codeDirc}ResultsToCSV_WTE.py" $subrates $recombination_rates $scalepopsize "${FastTreeDirc}FastTreeResultsWTE"

#Run FixedLength approach

#python3 "${codeDirc}FastTreeScriptCmdLine.py" $length $numberSubSamples $windowSizes $FastTreeSubFiles $Data $FastTreeDirc $dircOutput $codeDirc $LocationFastTree
wait


out="${FastTreeDirc}FixedLen.out"
err="${FastTreeDirc}FixedLen.err"

#nohup parallel -a "${dircOutput}cmdLineFastTree" -j $cores > $out 2> $err &
wait


#Compute RF for Fixed Length
<< ////

ls $Data | grep .newick > "${dircOutput}ListNewickFiles.txt"

numberLines="$(wc -l ${dircOutput}ListNewickFiles.txt)"


for word in $numberLines
do
        #echo $word
        num=$((word/cores))
        cd $dircOutput
        split -l $num --numeric-suffixes "${dircOutput}ListNewickFiles.txt" ListTreeFiles
        break
done

#split -l $numberLines "--numeric-suffixes " "${dircOutput}ListNewickFiles.txt"  ListTreeFiles
tempn=$((cores-1))

#for i in {0..$tempn};
for ((i=0; i <= $tempn; i++))
do
        #break
        echo $i
        if [ $((i < 10)) == 1 ];
        then
                num="0${i}"
                echo "first"
        else
                num="${i}"
                echo "second"
        fi
        temp="ListTreeFiles${num}"
        echo $temp
        python3 "${codeDirc}IqtreeProcessFT_InputFile_RF.py" "${dircOutput}${temp}" $Data $FastTreeDirc $windowSizes $subrates $numberSubSamples $length $codeDirc &
done

wait

////


python3 "${codeDirc}ResultsToCSV2.py" $subrates $recombination_rates $scalepopsize $FastTreeDirc "${FastTreeDirc}FixedLen_RF_All_Filtered" $windowSizes
wait


cd $FastTreeDirc
ls $FastTreeDirc | grep FixedLen_RF_All_Filtered | xargs -I {} cp {} $ResultsDirc
#ls $FastTreeDirc | grep FastTreeResultsWTE_ | xargs -I {} cp {} $ResultsDirc




