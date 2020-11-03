#! /bin/bash
typeFile=$1
indir=$2
force=""

if [ "${typeFile}" == "" ]
then
    typeFile="MC/backgrounds"
fi
outdir="lfvanalysis_rootfiles/${typeFile}"
outdir="root://cmseos.fnal.gov//store/user/mmackenz/"${outdir}

year=""
if [ "$4" != "" ]
then
    year=$4
fi

if [ "$2" == "" ]
then
    indir="./rootfiles/latest_production/${typeFile}/*${year}*.root"
else
    indir="${indir}/*${year}*.root"
fi
if [ "$3" == "" ]
then
    force=""
else
    force="-f "
fi


echo "Using input path ${indir} and output path ${outdir}"
for f in `ls ${indir}`; do echo "Copying tree file "${f}; xrdcp ${force}$f $outdir; done

echo "Finished moving trees! Remove local trees when confident there were no errors"
