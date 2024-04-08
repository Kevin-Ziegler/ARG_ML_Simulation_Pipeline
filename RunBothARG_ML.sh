#!/usr/bin/env bash

#CodeDirectory="/pool/Kevin81/RedoResults_10_12_2023/DryadPipeLine/"
#DataDirectory="/pool/Kevin81/RedoResults_10_12_2023/Data3/"

CodeDirectory=$1
DataDirectory=$2

mkdir $DataDirectory

ARGo="${DataDirectory}ARGrun.out"
ARGe="${DataDirectory}ARGrun.err"

MLo="${DataDirectory}MLrun.out"
MLe="${DataDirectory}MLrun.out"

#Runs Co-estimation methods
echo "Start ${DataDirectory} ARG"
./Run_ARG.sh $CodeDirectory $DataDirectory > $ARGo 2> $ARGe &
wait

echo "Start ${DataDirectory} ML"
#Runs ML method Fast Tree
./Run_ML.sh $CodeDirectory $DataDirectory > $MLo 2> $MLe &
wait




