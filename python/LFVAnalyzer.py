#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from StandardModel.ZEMuAnalysis.runSkimModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

inputFile = [ sys.argv[1] ]
isData = False
if sys.argv[2].split('=')[1] == "True":
    isData = True
year = sys.argv[3].split('=')[1]


# p=PostProcessor(".",inputfile,"",modules=[leptonConstr(0)],provenance=True,fwkJobReport=True,outputbranchsel="cmssw_config/keep_and_drop.txt")
if isData :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
else :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0),puAutoWeight_2016()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1),puAutoWeight_2017()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2),puAutoWeight_2018()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")

p.run()

print "LFVAnalyzer has finished file", inputFile[0]
