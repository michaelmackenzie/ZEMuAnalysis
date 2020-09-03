from CRABClient.UserUtilities import config
config = config()
 
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'ZEMuAnalysis_Pythia8_NANOAOD_2017_10218V2'
config.General.workArea = 'crab_projects'

config.section_('JobType')
config.JobType.psetName = 'cmssw_config/ZEMuAnalysis_13TeV_pythia8_NANOAOD_2017_LEGACY_cfg.py'
config.JobType.pluginName = 'Analysis'

config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDataset = '/ZEMuAnalysis_2017_934V1/pellicci-ZEMuAnalysis_MINIAOD_2017_946V1-4fe98f39b775e67c69bc92a03424ad6b/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publication = True

config.Data.outputDatasetTag = 'ZEMuAnalysis_NANOAOD_2017_10218V2'

config.section_('Site')
config.Site.storageSite = 'T2_IT_Bari'
