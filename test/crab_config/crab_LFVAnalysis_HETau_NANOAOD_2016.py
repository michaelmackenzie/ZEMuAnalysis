from CRABClient.UserUtilities import config
config = config() 

config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'LFVAnalysis_HETau_Pythia8_NANOAOD_2016_8028V1'
config.General.workArea = 'crab_projects'

config.section_('JobType')
config.JobType.psetName = 'cmssw_config/ZEMuAnalysis_13TeV_pythia8_NANOAOD_2016_cfg.py'
config.JobType.pluginName = 'Analysis'

config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset = '/LFVAnalysis_HETau_2016_8028V1/pellicci-LFVAnalysis_MINIAOD_949V1-53f8667ba4b240d5eafd36e71bf34742/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
config.Data.outLFNDirBase = '/store/user/mimacken/'
config.Data.publication = True

config.Data.outputDatasetTag = 'LFVAnalysis_NANOAOD_8028V1'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
