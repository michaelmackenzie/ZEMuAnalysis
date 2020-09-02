from CRABClient.UserUtilities import config
config = config() 

 # 
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'LFVAnalysis_HEMu_Pythia8_NANOAOD_2018_10218V1'
config.General.workArea = 'crab_projects'

config.section_('JobType')
config.JobType.psetName = 'cmssw_config/ZEMuAnalysis_13TeV_pythia8_NANOAOD_2018_cfg.py'
config.JobType.pluginName = 'Analysis'

config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset = '/LFVAnalysis_HEMu_2018_10218V1/pellicci-LFVAnalysis_MINIAOD_10218V1-54b8060d079e1ece71392c3e505d3426/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
config.Data.outLFNDirBase = '/store/user/mimacken/'
config.Data.publication = True

config.Data.outputDatasetTag = 'LFVAnalysis_NANOAOD_8028V1'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
