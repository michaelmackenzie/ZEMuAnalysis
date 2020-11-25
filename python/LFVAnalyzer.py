#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from StandardModel.ZEMuAnalysis.runSkimModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

inputFile = [ sys.argv[1] ]
isData = False
if sys.argv[2].split('=')[1] == "data":
    isData = True
year = sys.argv[3].split('=')[1]
saveZ = False #for saving Drell-Yan (or signal) Z info
if sys.argv[4].split('=')[1] == "True":
    saveZ = True
maxEvents = -1
startEvent = 1
if len(sys.argv) > 5: #additional parameter of max events
    maxEvents = int(sys.argv[5])
    print "Using maximum read events =", maxEvents
if len(sys.argv) > 6: #additional parameter of start event
    startEvent = int(sys.argv[6])
    print "Using initial event =", startEvent
print "LFVAnalyzer using input file", inputFile, "isData", isData, "year", year, "saveZ", saveZ

# p=PostProcessor(".",inputfile,"",modules=[leptonConstr(0)],provenance=True,fwkJobReport=True,outputbranchsel="cmssw_config/keep_and_drop.txt")
if isData :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0, maxEvents, startEvent, 1, False)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1, maxEvents, startEvent, 1, False)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2, maxEvents, startEvent, 1, False)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
else :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0, maxEvents, startEvent, 0, saveZ),puAutoWeight_2016()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1, maxEvents, startEvent, 0, saveZ),puAutoWeight_2017()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2, maxEvents, startEvent, 0, saveZ),puAutoWeight_2018()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")

p.run()

print "LFVAnalyzer has finished file", inputFile[0]
