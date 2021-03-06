from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_projects/GEN2016'

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.outputFiles = ['ZEMuAnalysis_pythia8_GENSIM_2016.root']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 5
NJOBS = 8000 #Do not increase: maximum number of jobs per task is 10k
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_IT_Bari'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    config.General.requestName = 'LFVAnalysis_ZEMu_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_ZEMu_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZEMu_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_ZEMu_GENSIM_2016_8028V1'

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.General.requestName = 'LFVAnalysis_ZETau_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_ZETau_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZETau_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_ZETau_GENSIM_2016_8028V1'
    
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.General.requestName = 'LFVAnalysis_ZMuTau_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_ZMuTau_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_ZMuTau_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_ZMuTau_GENSIM_2016_8028V1'

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.General.requestName = 'LFVAnalysis_HEMu_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_HEMu_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_HEMu_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_HEMu_GENSIM_2016_8028V1'

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.General.requestName = 'LFVAnalysis_HETau_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_HETau_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_HETau_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_HETau_GENSIM_2016_8028V1'
    
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.General.requestName = 'LFVAnalysis_HMuTau_GENSIM_2016_8028V1'
    config.JobType.psetName = 'LFVAnalysis_HMuTau_13TeV_pythia8_GENSIM_2016_cfg.py'
    config.Data.outputPrimaryDataset = 'LFVAnalysis_HMuTau_2016_8028V1'
    config.Data.outputDatasetTag = 'LFVAnalysis_HMuTau_GENSIM_2016_8028V1'

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()
