#!/usr/bin/env bash

dircOutput="/pool/Kevin81/RedoResults_10_12_2023/Data2/"
length="1000"
codeDirc="/pool/Kevin81/RedoResults_10_12_2023/DryadPipeLine/"
cores=30
numberSubSamples=1

#Must be in decesending order or will not work
#windowSizes=5000,2500,1250,625,312
windowSizes=625,312
subrates=0.0001,0.0000001,0.000000001
recombination_rates=8.0,2.0,1.0,0.125
scalepopsize=8.0,1.0,0.125

:'
subrates=0.0001,0.00003162277,0.00001,0.00000316227,0.000001,0.000000316227,0.0000001,0.0000000316227,0.00000001,0.00000000316227,0.000000001
recombination_rates=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
scalepopsize=16.0,8.0,4.0,2.0,1.0,0.5,0.25,0.125,0.0625
'


LocationFastTree="/pool/Kevin81/BackUpDriveCode_2018_2021/Programs/FastTree"



FastTreeDirc="${dircOutput}FastTree/"
FastTreeSubFiles="${FastTreeDirc}SubFiles/"
ResultsDirc="${dircOutput}Results/"

mkdir $FastTreeDirc
mkdir $FastTreeSubFiles
mkdir $ResultsDirc

Data="${dircOutput}Data/"


cd $Data

ls | grep .phy$ > ../ListWTEFiles.txt

cd ..

numberLinesWTE="$(wc -l ListWTEFiles.txt)"


#Old file split version
#For loop needed because wc -l  returns two things: numlines filename
#for word in $numberLinesWTE
#do
#        #echo $word
#        num=$((word/cores))
#	num=$((num+1))
#        #cd $dircOutput
#        #split -l $num --numeric-suffixes "ListWTEFiles.txt" ListTreeFilesWTE
#        break
#done


#New file split version
input_file=ListWTEFiles.txt
output_prefix="ListTreeFilesWTE"
#cores=8  # Set the number of cores

line_number=0

while IFS= read -r line; do
    ((line_number++))

    # Calculate the subfile number based on the current line
    subfile_number=$((line_number % cores))

    # Format the subfile number as two digits
    subfile_number_formatted=$(printf "%02d" "$subfile_number")

    subfile_name="${output_prefix}${subfile_number_formatted}"
    echo "$line" >> "$subfile_name"
done < "$input_file"



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
        temp="ListTreeFilesWTE${num}"
        tempo="ListTreeFilesWTE${num}.out"
        tempe="ListTreeFilesWTE${num}.err"
        echo $temp
        #python3 "${codeDirc}IqtreeProcessFT_InputFile_RF.py" "${dircOutput}${temp}" $Data $FastTreeDirc $windowSizes $subrates $numberSubSamples $length $codeDirc &
        #Run ML with Estimated and True Breakpoints along with the whole length
        python3 "${codeDirc}FastTreeWholeEstTrue.py" $dircOutput $length $codeDirc $LocationFastTree $temp > "${dircOutput}${tempo}" 2> "${dircOutput}${tempe}" &
done
wait


#Run ML with Estimated and True Breakpoints along with the whole length

python3 "${codeDirc}FastTreeResultsWTE.py" $FastTreeDirc
wait

python3 "${codeDirc}ResultsToCSV_WTE.py" $subrates $recombination_rates $scalepopsize "${FastTreeDirc}FastTreeResultsWTE"


#Fixed Length
python3 "${codeDirc}FastTreeScriptCmdLine.py" $length $numberSubSamples $windowSizes $FastTreeSubFiles $Data $FastTreeDirc $dircOutput $codeDirc $LocationFastTree
wait


out="${FastTreeDirc}FixedLen.out"
err="${FastTreeDirc}FixedLen.err"

nohup parallel -a "${dircOutput}cmdLineFastTree" -j $cores > $out 2> $err &
wait



#Compute RF for Fixed Length

ls $Data | grep .newick > "${dircOutput}ListNewickFiles.txt"

numberLines="$(wc -l ${dircOutput}ListNewickFiles.txt)"


#old file split
#for word in $numberLines
#do
#        #echo $word
#        num=$((word/cores))
#	num=$((num+1))
#        cd $dircOutput
#        split -l $num --numeric-suffixes "${dircOutput}ListNewickFiles.txt" ListTreeFiles
#        break
#done

#new split


input_file=ListNewickFiles.txt
output_prefix="ListTreeFiles"
#cores=8  # Set the number of cores

line_number=0

while IFS= read -r line; do
    ((line_number++))

    # Calculate the subfile number based on the current line
    subfile_number=$((line_number % cores))

    # Format the subfile number as two digits
    subfile_number_formatted=$(printf "%02d" "$subfile_number")

    subfile_name="${output_prefix}${subfile_number_formatted}"
    echo "$line" >> "$subfile_name"
done < "$input_file"


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
	tempo="ListTreeFiles${num}.out"
	tempe="ListTreeFiles${num}.err"
        echo $temp
        python3 "${codeDirc}IqtreeProcessFT_InputFile_RF.py" "${dircOutput}${temp}" $Data $FastTreeDirc $windowSizes $subrates $numberSubSamples $length $codeDirc > "${dircOutput}${tempo}" 2> "${dircOutput}${tempe}" &
done

wait


cd $FastTreeDirc
ls $FastTreeDirc | grep "FixedLen_RF_" | grep -v "FixedLen_RF_All" | xargs -I {} cat {} > "FixedLen_RF_All"
wait



echo "Hello"

python3 "${codeDirc}ResultsToCSV2.py" $subrates $recombination_rates $scalepopsize $FastTreeDirc "${FastTreeDirc}FixedLen_RF_All" $windowSizes
wait


cd $FastTreeDirc
ls $FastTreeDirc | grep FixedLen_RF_All_ | xargs -I {} cp {} $ResultsDirc
ls $FastTreeDirc | grep FastTreeResultsWTE_ | xargs -I {} cp {} $ResultsDirc


