#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from StandardModel.ZEMuAnalysis.qcdTestModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

inputFile = [ sys.argv[1] ]
isData = False
if sys.argv[2].split('=')[1] == "data":
    isData = True
year = sys.argv[3].split('=')[1]
maxEvents = -1
startEvent = 1
if len(sys.argv) > 4: #additional parameter of max events
    maxEvents = int(sys.argv[4])
    print "Using maximum read events =", maxEvents
if len(sys.argv) > 5: #additional parameter of start event
    startEvent = int(sys.argv[5])
    print "Using initial event =", startEvent
print "QCDTestAnalyzer using input file", inputFile, "year", year

if isData :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0, maxEvents, startEvent, 1)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1, maxEvents, startEvent, 1)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2, maxEvents, startEvent, 1)],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
else :
    if year == "2016" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(0, maxEvents, startEvent, 0),puAutoWeight_2016()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(1, maxEvents, startEvent, 0),puAutoWeight_2017()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,"", modules=[leptonConstr(2, maxEvents, startEvent, 0),puAutoWeight_2018()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/keep_and_drop.txt")

p.run()

print "QCDTestAnalyzer has finished file", inputFile[0]
