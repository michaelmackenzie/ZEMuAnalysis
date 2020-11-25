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
p.add_argument('isData_option', help='Type <<MC>> or <<data>>')
p.add_argument('year_option', help='Type <<2016>>, <<2017>> or <<2018>>')
p.add_argument('tag_option', help='Type e.g. <<LFVAnalysis>>')
args = p.parse_args()

onlySignalMC = False
tag="LFVAnalysis"
if args.isData_option == "MC":
    isData = False
elif args.isData_option == "data":
    isData = True
else:
    print "Option one should be MC or data! Defaulting to MC"
    isData = False
year = args.year_option
if year != "2016" and year != "2017" and year != "2018":
    print "Option two should be 2016, 2017, or 2018! Defaulting to 2016"
    year = "2016"
if args.tag_option != "":
    tag=args.tag_option
#---------------------------------#

if not os.path.exists("rootfiles"):
    os.makedirs("rootfiles")
if not os.path.exists("rootfiles/latest_production"):
    os.makedirs("rootfiles/latest_production")
if not os.path.exists("rootfiles/latest_production/MC"):
    os.makedirs("rootfiles/latest_production/MC")
if not os.path.exists("rootfiles/latest_production/dataprocess"):
    os.makedirs("rootfiles/latest_production/dataprocess")

print "Processing", args.isData_option, "for year", year, "with tag", tag

if not isData :
    dir_input = "crab_projects/samples_MC_" + year + "/"
    dir_output_bkg = "rootfiles/latest_production/MC/backgrounds/"
    dir_output_sig = "rootfiles/latest_production/MC/signals/"  
else :
    dir_input = "crab_projects/samples_data_" + year + "/"
    dir_output_data = "rootfiles/latest_production/dataprocess/"

list_dirs = os.listdir(dir_input)

if not isData and not os.path.exists(dir_output_bkg):
    os.makedirs(dir_output_bkg)

if not isData and not os.path.exists(dir_output_sig):
    os.makedirs(dir_output_sig)

if isData and not os.path.exists(dir_output_data):
    os.makedirs(dir_output_data)
for dirname in list_dirs:

    print "Processing sample dir " + dirname
    if "ZEMuAnalysis" in dirname:
        print "Old project name still used in " + dirname +"! Continuing..."
        continue
    if not tag in dirname:
        print "Skipping dataset!"
        continue
    
    isSignal = "EMu" in dirname or "ETau" in dirname or "MuTau" in dirname

    if onlySignalMC and not isSignal:
        print "Skipping background MC!"
        continue
    
    n_jobs_command = "crab status -d " + dir_input + dirname + " | grep status: " + "| awk " + """'{split($0,array,"/") ; print array[2]}'""" + "| sed 's/.$//'"
    n_jobs = int(subprocess.check_output(n_jobs_command, shell=True))

    print "Number of jobs to be retrieved: ", n_jobs
    n_trees_command = "ls " + dir_input + dirname + "/results/ | grep .root | wc | awk '{print $1}'"
    n_trees = int(subprocess.check_output(n_trees_command, shell=True))
    
    crab_command = "crab getoutput -d " + dir_input + dirname

    if n_trees == 0 : #only get the output if there aren't trees in the directory
        os.system(crab_command)
    else :
        print "Trees are already present, skipping getoutput command!"
    
    samplename = dirname.split("crab_" + year + "_" + tag + "_")

    if isSignal:
        hadd_command = "../scripts/haddnano.py " + dir_output_sig + "LFVAnalysis_" + samplename[1] + "_" + year + ".root " + dir_input + dirname + "/results/*.root"
    elif isData:
        hadd_command = "../scripts/haddnano.py " + dir_output_data + "LFVAnalysis_" + samplename[1] + "_" + year + ".root " + dir_input + dirname + "/results/*.root"
    else:
        hadd_command = "../scripts/haddnano.py " + dir_output_bkg + "LFVAnalysis_" + samplename[1] + "_" + year + ".root " + dir_input + dirname + "/results/*.root"

    os.system(hadd_command)

    # if not isSignal and not isData:
    #     p_Signal=PostProcessor(".",[dir_output_bkg + "LFVAnalysis_" + samplename[1] + "_" + year + ".root "],modules=[SignalFilter()],haddFileName=dir_output_bkg + "LFVAnalysis_" + samplename[1] + "_SigRegion_" + year + ".root ")
    #     p_Signal.run()
    # elif isData :
    #     p_Signal=PostProcessor(".",[dir_output_data + "LFVAnalysis_" + samplename[1] + "_" + year + ".root "],modules=[SignalFilter()],haddFileName=dir_output_data + "LFVAnalysis_" + samplename[1] + "_SigRegion_" + year + ".root ")
    #     p_Signal.run()


# Now treat and merge samples
if isData:
    hadd_command = "../scripts/haddnano.py " + dir_output_data + "LFVAnalysis_SingleMu_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleMu_?_" + year + ".root"
    rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleMu_?_" + year + ".root"

    os.system(hadd_command)
    os.system(rm_command)

    hadd_command = "../scripts/haddnano.py " + dir_output_data + "LFVAnalysis_SingleEle_DoubleTrig_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleEle_?_" + year + ".root"
    rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleEle_?_" + year + ".root"

    os.system(hadd_command)
    os.system(rm_command)
    #for HLTElectronFilter, pass running era
    if year == "2016" :
        runningEra = 0
    elif year == "2017" :
        runningEra = 1
    else :
        runningEra = 2

    p_HLT=PostProcessor(".",[dir_output_data + "LFVAnalysis_SingleEle_DoubleTrig_" + year + ".root "],modules=[HLTElectronFilter(runningEra)],haddFileName=dir_output_data + "LFVAnalysis_SingleEle_" + year + ".root ")
    p_HLT.run()

    rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleEle_DoubleTrig_" + year + ".root "
    os.system(rm_command)

    # p_Signal_mu=PostProcessor(".",[dir_output_data + "LFVAnalysis_SingleMu_" + year + ".root "],modules=[SignalFilter()],haddFileName=dir_output_data + "LFVAnalysis_SingleMu_SigRegion_" + year + ".root ")
    # p_Signal_mu.run()

    # p_Signal_ele=PostProcessor(".",[dir_output_data + "LFVAnalysis_SingleEle_" + year + ".root "],modules=[SignalFilter()],haddFileName=dir_output_data + "LFVAnalysis_SingleEle_SigRegion_" + year + ".root ")
    # p_Signal_ele.run()

print "All done!"
