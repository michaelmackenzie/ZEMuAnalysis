#! /usr/bin/env python
import StandardModel.ZEMuAnalysis.BatchMaster as bm

import os, sys


# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch.sh'
analyzer   = 'LFVAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/nano_batchout'
location   = 'lpc'



# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}



nEvtPerJob = 3 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 

#################################################
#                                               #
#---------------  Running data   ---------------#
#                                               #
#################################################
# dataset, nEvtPerJobIn1e6, year, isData, suffix


# Single Electron
samplesDict['2016_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, '2016_SingleElectronRun2016B'),
    bm.JobConfig( '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016C'),
    bm.JobConfig( '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016D'),
    bm.JobConfig( '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016E'),
    bm.JobConfig( '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016F'),
    bm.JobConfig( '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016G'),
    bm.JobConfig( '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleElectronRun2016H')]

samplesDict['2017_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleElectronRun2017B'),
    bm.JobConfig( '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleElectronRun2017C'),
    bm.JobConfig( '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleElectronRun2017D'),
    bm.JobConfig( '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleElectronRun2017E'),
    bm.JobConfig( '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleElectronRun2017F')]

samplesDict['2018_SingleElectron'] = [
    bm.JobConfig( '/EGamma/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleElectronRun2018A'),
    bm.JobConfig( '/EGamma/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleElectronRun2018B'),
    bm.JobConfig( '/EGamma/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleElectronRun2018C'),
    bm.JobConfig( '/EGamma/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleElectronRun2018D')]



# Single Muon
samplesDict['2016_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, '2016_SingleMuonRun2016B'),
    bm.JobConfig( '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016C'),
    bm.JobConfig( '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016D'),
    bm.JobConfig( '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016E'),
    bm.JobConfig( '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016F'),
    bm.JobConfig( '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016G'),
    bm.JobConfig( '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, '2016_SingleMuonRun2016H')]

samplesDict['2017_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleMuonRun2017B'),
    bm.JobConfig( '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleMuonRun2017C'),
    bm.JobConfig( '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleMuonRun2017D'),
    bm.JobConfig( '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleMuonRun2017E'),
    bm.JobConfig( '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, '2017_SingleMuonRun2017F')]

samplesDict['2018_SingleMuon'] = [
    bm.JobConfig( '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleMuonRun2018A'),
    bm.JobConfig( '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleMuonRun2018B'),
    bm.JobConfig( '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleMuonRun2018C'),
    bm.JobConfig( '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, '2018_SingleMuonRun2018D')]





### redefine N(events/job) for MC ###
nEvtPerJob = 3

#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################

# top
samplesDict['2016_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='2016_LFVAnalysis_ttbarToSemiLeptonic'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='2016_LFVAnalysis_ttbarlnu'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='2016_LFVAnalysis_ttbarToHadronic'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='2016_LFVAnalysis_SingleToptW'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='2016_LFVAnalysis_SingleAntiToptW'),
]

# w
samplesDict['2016_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_Wlnu'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_Wlnu-ext'),


    # # w1jets inclusive
    # bm.JobConfig( 
    # dataset='/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
    # nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_W1Jets'),
    # # w2jets inclusive
    # bm.JobConfig( 
    # dataset='/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
    # nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_W2Jets'),
    # # w3jets inclusive
    # bm.JobConfig( 
    # dataset='/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
    # nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_W3Jets'),
    # # w4jets inclusive
    # bm.JobConfig( 
    # dataset='/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
    # nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_W4Jets'),
     
]

# z
samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_DY50'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_DY50-ext'),    
]

# di(tri)-boson
samplesDict['2016_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_WW'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_WWLNuQQ'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_WZ'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_ZZ'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_WWW'),
]

# qcd
samplesDict['2016_qcd'] = [
    # 30-40
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_QCDDoubleEMEnrich30to40'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_QCDDoubleEMEnrich30toInf'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=0, suffix='2016_LFVAnalysis_QCDDoubleEMEnrich40toInf'),
]

#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# top
samplesDict['2017_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='2017_LFVAnalysis_ttbarToSemiLeptonic'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='2017_LFVAnalysis_ttbarlnu'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v2/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='2017_LFVAnalysis_ttbarToHadronic'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='2017_LFVAnalysis_SingleToptW'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='2017_LFVAnalysis_SingleAntiToptW'),
]

# w
samplesDict['2017_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_Wlnu'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_Wlnu-ext'),
]

# z
samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_DY50'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_DY50-ext'),    
]

# di(tri)-boson
samplesDict['2017_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_WW'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_WWLNuQQ'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_WZ'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_ZZ'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_WWW'),
]

# qcd
samplesDict['2017_qcd'] = [
    # 30-40
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_QCDDoubleEMEnrich30to40'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_QCDDoubleEMEnrich30toInf'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=0, suffix='2017_LFVAnalysis_QCDDoubleEMEnrich40toInf'),
]

#################################################
#                                               #
#--------------- Running 2018 MC ---------------#
#                                               #
#################################################
# top
samplesDict['2018_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='2018_LFVAnalysis_ttbarToSemiLeptonic'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='2018_LFVAnalysis_ttbarlnu'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='2018_LFVAnalysis_ttbarToHadronic'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='2018_LFVAnalysis_SingleToptW'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='2018_LFVAnalysis_SingleAntiToptW'),
]

# w
samplesDict['2018_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_Wlnu'),

    # bm.JobConfig( 
    #     dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_Wlnu-ext'),
]

# z
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_DY50'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_DY50-ext'),    
]

# di(tri)-boson
samplesDict['2018_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_WW'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_WWLNuQQ'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_WZ'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_ZZ'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_WWW'),
]

# qcd
samplesDict['2018_qcd'] = [
    # 30-40
    # bm.JobConfig(
    #     dataset='', #None found in DAS...
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_QCDDoubleEMEnrich30to40'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_QCDDoubleEMEnrich30toInf'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=0, suffix='2018_LFVAnalysis_QCDDoubleEMEnrich40toInf'),
]

# -----------------------------
# submit to batch
# -----------------------------
samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()
doYears = ["2017"] #["2016" , "2017", "2018" ]
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears:
        configs += samplesDict[s]

batchMaster = bm.BatchMaster(
    analyzer    = analyzer,
    config_list = configs, 
    stage_dir   = stage_dir,
    output_dir  = output_dir,
    executable  = executable,
    location    = location
)

#ensure there's a symbolic link 'batch' to put the tarball in
if not os.path.exists("batch") :
    if not os.path.exists("~/nobackup/batch") :
        os.makedirs("~/nobackup/batch")
    os.symlink("~/nobackup/batch", "batch")
    print "Created symbolic link to ~/nobackup/batch"

batchMaster.submit_to_batch(doSubmit=True)
