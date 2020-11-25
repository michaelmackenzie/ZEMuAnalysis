#!/bin/sh

echo "Job submitted on host `hostname` on `date`"
echo ">>> arguments: $@"

### Required parameters #####
COUNT=$1
YEAR=$2
SUFFIX=$4
OUTDIR=$5
ANALYZER=$6

if [[ "$3" == "True" ]]
then
    ISDATA="data"
else
    ISDATA="MC"
fi

### Transfer files, prepare directory ###
TOPDIR=$PWD

# lpc
export SCRAM_ARCH=slc7_amd64_gcc700
export CMSSW_VERSION=CMSSW_10_2_18
source /cvmfs/cms.cern.ch/cmsset_default.sh

# temporary fix
tar -xzf source.tar.gz
mv $CMSSW_VERSION tmp_source
scram project CMSSW $CMSSW_VERSION
cp -r tmp_source/src/* $CMSSW_VERSION/src
cd $CMSSW_VERSION/src
eval `scram runtime -sh`

# this used to work, now it don't
#tar -xzf source.tar.gz
#cd $CMSSW_VERSION/src/
#scramv1 b ProjectRename

cmsenv
scramv1 b -j8 #ProjectRename
# cd BLT/BLTAnalysis/scripts
INPUT_TXT_FILENAME=input_${SUFFIX}_${COUNT}.txt
cp $TOPDIR/${INPUT_TXT_FILENAME} ${INPUT_TXT_FILENAME}

echo "Inputs: "
echo $ANALYZER $SUFFIX $YEAR $ISDATA $COUNT 
echo "PATH: "
echo $PATH
echo "Starting working dir: "
pwd
cd StandardModel/ZEMuAnalysis
echo "Working dir: "
pwd
mv ../../input_${SUFFIX}_${COUNT}.txt ./
echo "Input file list: "
cat $INPUT_TXT_FILENAME


[ ! -d outDir ] && mkdir outDir

### Run the analyzer

COUNTER=0
while IFS= read NANOAOD
do
    # xrdcp to local src folder first
    # analyzer is upto 100x-200x faster than xrd streaming. Ziheng
    echo "Copying ${NANOAOD} locally"
    xrdcp ${NANOAOD} ./temp.root
    saveZ="False"
    if [[ ${NANOAOD} == *"DYJets"* ]] || [[ ${NANOAOD} == *"ZEMu"* ]] ||  [[ ${NANOAOD} == *"ZETau"* ]] ||  [[ ${NANOAOD} == *"ZMuTau"* ]]
    then
	saveZ="True"
    fi
    echo "Save Z info = ${saveZ}"
    python python/${ANALYZER}.py temp.root isData=${ISDATA} year=${YEAR} saveZ=${saveZ}
    mv tree.root outDir/tree_${COUNTER}.root
    rm *.root
    COUNTER=$((COUNTER+1))

done <$INPUT_TXT_FILENAME

ls
ls outDir/

### Copy output and cleanup ###
FILE=output_${SUFFIX}_${COUNT}.root
scripts/haddnano.py ${FILE} outDir/*root

xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1
XRDEXIT=$?
if [[ $XRDEXIT -ne 0 ]]; then
  rm *.root
  echo "exit code $XRDEXIT, failure in xrdcp"
  exit $XRDEXIT
fi
rm ${FILE}
rm -rf outDir

