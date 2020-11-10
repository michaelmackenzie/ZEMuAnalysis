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
    bm.JobConfig( '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016B_2016'),
    bm.JobConfig( '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016C_2016'),
    bm.JobConfig( '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016D_2016'),
    bm.JobConfig( '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016E_2016'),
    bm.JobConfig( '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016F_2016'),
    bm.JobConfig( '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016G_2016'),
    bm.JobConfig( '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016H_2016')]

samplesDict['2017_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017B_2017'),
    bm.JobConfig( '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017C_2017'),
    bm.JobConfig( '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017D_2017'),
    bm.JobConfig( '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017E_2017'),
    bm.JobConfig( '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017F_2017')]

samplesDict['2018_SingleElectron'] = [
    bm.JobConfig( '/EGamma/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018A_2018'),
    bm.JobConfig( '/EGamma/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018B_2018'),
    bm.JobConfig( '/EGamma/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018C_2018'),
    bm.JobConfig( '/EGamma/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018D_2018')]



# Single Muon
samplesDict['2016_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016B_2016'),
    bm.JobConfig( '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016C_2016'),
    bm.JobConfig( '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016D_2016'),
    bm.JobConfig( '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016E_2016'),
    bm.JobConfig( '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016F_2016'),
    bm.JobConfig( '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016G_2016'),
    bm.JobConfig( '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016H_2016')]

samplesDict['2017_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017B_2017'),
    bm.JobConfig( '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017C_2017'),
    bm.JobConfig( '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017D_2017'),
    bm.JobConfig( '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017E_2017'),
    bm.JobConfig( '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017F_2017')]

samplesDict['2018_SingleMuon'] = [
    bm.JobConfig( '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018A_2018'),
    bm.JobConfig( '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018B_2018'),
    bm.JobConfig( '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018C_2018'),
    bm.JobConfig( '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018D_2018')]





### redefine N(events/job) for MC ###
nEvtPerJob = 2

#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2016_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/ZEMuAnalysis_2016_8028V1/pellicci-ZEMuAnalysis_NANOAOD_10218V1-b1c578360797952dfc156561d5f36519/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZEMu_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZETau_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZMuTau_2016', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_HEMu_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_HETau_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_HMuTau_2016', inputDBS="phys03"),
]

# top
samplesDict['2016_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2016'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarlnu_2016'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2016'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleToptW_2016'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2016'),
]

# w
samplesDict['2016_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu_2016'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-ext_2016'),

]

# z
samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY50_2016'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY50-ext_2016'),    
]

# di(tri)-boson
samplesDict['2016_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WW_2016'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WWLNuQQ_2016'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WZ_2016'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZZ_2016'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WWW_2016'),
]

# qcd
samplesDict['2016_qcd'] = [
    # 30-40
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2016'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2016'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2016'),
]

#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2017_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZEMu_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZETau_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZMuTau_2017', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_HEMu_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_HETau_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_HMuTau_2017', inputDBS="phys03"),
]

# top
samplesDict['2017_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2017'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarlnu_2017'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v2/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2017'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleToptW_2017'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2017'),
]

# w
samplesDict['2017_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu_2017'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-ext_2017'),
]

# z
samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_DY50_2017'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_DY50-ext_2017'),    
]

# di(tri)-boson
samplesDict['2017_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WW_2017'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WWLNuQQ_2017'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WZ_2017'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZZ_2017'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WWW_2017'),
]

# qcd
samplesDict['2017_qcd'] = [
    # 30-40
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2017'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2017'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2017'),
]

#################################################
#                                               #
#--------------- Running 2018 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2018_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZEMu_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZETau_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZMuTau_2018', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_HEMu_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_HETau_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_HMuTau_2018', inputDBS="phys03"),
]

# top
samplesDict['2018_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2018'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarlnu_2018'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2018'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleToptW_2018'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2018'),
]

# w
samplesDict['2018_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu_2018'),
]

# z
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_DY50_2018'),
]

# di(tri)-boson
samplesDict['2018_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WW_2018'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WWLNuQQ_2018'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WZ_2018'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZZ_2018'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WWW_2018'),
]

# qcd
samplesDict['2018_qcd'] = [
    # 30-40
    # bm.JobConfig(
    #     dataset='', #None found in DAS...
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2018'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2018'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2018'),
]

# -----------------------------
# submit to batch
# -----------------------------
samplesToSubmit = ["2017_top", "2017_z", "2017_w", "2017_vv", "2017_qcd"]
# samplesToSubmit = samplesDict.keys()
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
