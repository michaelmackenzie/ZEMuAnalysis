#! /bin/bash

sample=$1
year=$2
for fIn in `ls -d crab_projects/samples_${sample}_${year}/crab_${year}_ZEMuAnalysis_*`
do
    echo $fIn
    fOut=${fIn//ZEMu/LFV}
    echo $fOut
    [ -d "${fOut}" ] && rm -r $fOut
    mv $fIn $fOut
done
rename "Signal" "ZEMu" crab_projects/samples_MC_${year}/crab_*Signal
