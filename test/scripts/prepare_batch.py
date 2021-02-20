import ROOT
import os, sys
import subprocess
import argparse
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

ROOT.PyConfig.IgnoreCommandLineOptions = True

class HLTElectronFilter(Module):
    def __init__(self,runningEra):
	self.writeHistFile=True
        self.runningEra = runningEra

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

    def analyze(self, event):

        HLT = Object(event, "HLT") 
        # if no muon trigger, not in muon data stream
        if not (HLT.IsoMu24 or HLT.IsoMu27 or HLT.Mu50) :
            return True
        muons = Collection(event, "Muon")
        # check if would pass muon trigger requirements
        for index in range(len(muons)):
            if (((HLT.IsoMu24 and muons[index].pt > 25. and self.runningEra != 1) or
                 (HLT.IsoMu27 and muons[index].pt > 28. and self.runningEra == 1) or
                 (HLT.Mu50 and muons[index].pt > 50.)) and
                muons[index].tightId and muons[index].pfRelIso04_all < 0.15):
                return False
        # fails muon trigger requirements, so must have passed only electron trigger requirements
        return True

class SignalFilter(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

    def analyze(self, event):

        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")

        if (len(muons) == 0 or len(electrons) == 0) :
            return False

        return True

#---------------------------------#
p = argparse.ArgumentParser(description='Select whether to download MC or data')
p.add_argument('input_dir', help='Type e.g. input file path')
p.add_argument('output_dir', help='Type e.g. output file path')
args = p.parse_args()

inputpath = args.input_dir
outputpath = args.output_dir
if outputpath == "":
    outputpath = "lfvanalysis_rootfiles/"
#---------------------------------#

print "Processing input path", inputpath, "to output path", outputpath

dir_output_data = outputpath + "dataprocess/"
dir_output_bkg  = outputpath + "MC/backgrounds/"
dir_output_sig  = outputpath + "MC/signals/"

list_dirs = os.listdir(inputpath) #list all first files to get 1 per dataset
list_processed = []
for dirname in list_dirs:

    samplename = dirname.split("_")
    outputname = ""
    for index in range(len(samplename)-1):        
        if index > 0:
            outputname = outputname + "_"
        outputname = outputname + samplename[index]
    outputname = outputname
    if outputname in list_processed:
        continue
    list_processed.append(outputname)
    print "Processing dataset", outputname
    
    isSignal = "EMu_" in dirname or "ETau_" in dirname or "MuTau_" in dirname
    isData = "SingleElectron" in dirname or "SingleMuon" in dirname

    inputname = outputname + "_*.root"
    outputname = outputname.replace("output_" ,"")
    outputname = outputname + ".root"
    if isSignal:
        hadd_command = "./haddnano.py " + dir_output_sig  + outputname + " " + inputpath + inputname
    elif isData:
        hadd_command = "./haddnano.py " + dir_output_data + outputname + " " + inputpath + inputname
    else:
        hadd_command = "./haddnano.py " + dir_output_bkg  + outputname + " " + inputpath + inputname

    print hadd_command
    os.system(hadd_command)


print "Finishing initial merging! Now merging data run sections..."
# Now treat and merge samples
for year in ["2016", "2017", "2018"]:
    doSingleMu = False
    for dataset in list_processed:
        if "SingleMuonRun"+year in dataset:
            doSingleMu = True
            break
    doSingleEle = False
    for dataset in list_processed:
        if "SingleElectronRun"+year in dataset:
            doSingleEle = True
            break
    if doSingleMu:
        hadd_command = "date +\"%r\"; ./haddnano.py " + dir_output_data + "LFVAnalysis_SingleMu_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleMuonRun" + year + "*.root"
        rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleMuonRun" + year + "*.root"
        print hadd_command
        # print rm_command
        os.system(hadd_command)
        # os.system(rm_command)
    if doSingleEle:
        hadd_command = "./haddnano.py " + dir_output_data + "LFVAnalysis_SingleEle_DoubleTrigger_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleElectronRun" + year + "*.root"
        rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleElectronRun" + year + "*.root"

        print hadd_command
        print rm_command
        os.system(hadd_command)
        os.system(rm_command)

        #for HLTElectronFilter, pass running era
        if year == "2016" :
            runningEra = 0
        elif year == "2017" :
            runningEra = 1
        else :
            runningEra = 2

        print "Running electron data filtering!"
        p_HLT=PostProcessor(".",[dir_output_data + "LFVAnalysis_SingleEle_DoubleTrigger_" + year + ".root "],modules=[HLTElectronFilter(runningEra)],haddFileName=dir_output_data + "LFVAnalysis_SingleEle_" + year + ".root ")
        p_HLT.run()

        print "Finished electron data filtering!"
        rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleEle_DoubleTrigger_" + year + ".root "
        print rm_command
        os.system(rm_command)
        print "Copying local Electron skimmed version to output"
        mv_command = "mv " + "LFVAnalysis_SingleEle_DoubleTrigger_" + year + "_Skim.root " + dir_output_data + "LFVAnalysis_SingleEle_" + year + ".root"
        print mv_command
        os.system(mv_command)
        
        
print "All done!"
