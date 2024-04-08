#!/usr/bin/env bash

# whichpython=python3
# outputdirc=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCFiles/
# outputdirc2=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCOutput/
# length=100000
# dircName=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/April_8_2020/
# Script1=/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/KendallColijnPrep.py
# Script2=/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/KendallColijn.r
# Script3=/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/CreateResultsRentPlus.py
# outFile=/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentResults


whichpython=$1
RentPlusDirectory=$2
length=$3
DataDirectory=$4
cores=$5
CodeDirectory=$6
popSize=$7
what=$8



echo "In Solution Pipe"

echo $whichpython
echo $RentPlusDirectory
echo $length
echo $DataDirectory
echo $cores
echo $CodeDirectory
echo $popSize
echo $what



Script1="${CodeDirectory}KendallColijnPrep.py"
Script2="${CodeDirectory}RentPlus_RF.r"
Script3="${CodeDirectory}CreateResultsRentPlus.py"

outFile="${RentPlusDirectory}AllResults"


outputdirc="${RentPlusDirectory}PrepFiles/"
outputdirc2="${RentPlusDirectory}OutputFiles/"

mkdir $outputdirc
mkdir $outputdirc2

echo "Path to Kendall Colijn Prep"
echo $CodeDirectory
echo $Script1

cd $outputdirc
echo $outputdirc
echo $length
echo $DataDirectory

$whichpython $Script1 $outputdirc $length $DataDirectory


ls $outputdirc > FileNames.txt
#numFiles=$(ls $outputdirc | wc -l)
#linesPerFile=$(expr $numFiles / $cores)
#echo "lines per file"
#echo $linesPerFile
#split -l $linesPerFile FileNames.txt splitF -d

#Split files evenly, with entries distributed evenly. Code from chat gpt
input_file=FileNames.txt
output_prefix="splitF"

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

fileLst=$(ls | grep splitF | grep -v .out | grep -v .err)
echo $fileLst

for f in $fileLst
do
	echo $f
	temp1="${f}.out"
	temp2="${f}.err"
	#nohup Rscript $Script2 $outputdirc $outputdirc2 $file > $temp1 2> $temp2 < /dev/null &
	temp3="${outputdirc}${f}"
	echo $temp3
	#Rscript $Script2 $outputdirc $outputdirc2 $temp3
	nohup Rscript $Script2 $outputdirc $outputdirc2 $temp3 $popSize > $temp1 2> $temp2 < /dev/null &
done

wait
#must wait for command to complete

$whichpython $Script3 $outputdirc $outputdirc2 $outFile

wait

