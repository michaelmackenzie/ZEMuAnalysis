from CRABClient.UserUtilities import config
from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferLogs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_config/crab_script.sh'
config.JobType.inputFiles = ['crab_config/crab_script.py','../scripts/haddnano.py','cmssw_config/keep_and_drop.txt']
config.JobType.sendPythonFolder	 = True

config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.outputDatasetTag = None
config.Data.outLFNDirBase = '/store/user/mimacken/zemu_nanoaod/'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC' # Choose your site. 

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

    ################### 2016 Samples #########################

    ##### Z samples #####
    
    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_ZEMuAnalysis_Signal'
    config.Data.inputDataset = '/ZEMuAnalysis_2016_8028V1/pellicci-ZEMuAnalysis_NANOAOD_10218V1-b1c578360797952dfc156561d5f36519/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_LFVAnalysis_ZETau'
    config.Data.inputDataset =  '/LFVAnalysis_ZETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_LFVAnalysis_ZMuTau'
    config.Data.inputDataset =  '/LFVAnalysis_ZMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    ##### H samples #####

    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_LFVAnalysis_HEMu'
    config.Data.inputDataset =  '/LFVAnalysis_HEMu_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_LFVAnalysis_HETau'
    config.Data.inputDataset =  '/LFVAnalysis_HETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_LFVAnalysis_HMuTau'
    config.Data.inputDataset =  '/LFVAnalysis_HMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    ################### 2017 Samples #########################

    # config.JobType.scriptArgs = ['isData=MC','year=2017']
    # config.General.workArea = 'crab_projects/samples_MC_2017/'
    # config.General.requestName = '2017_ZEMuAnalysis_Signal'
    # config.Data.inputDataset = '/ZEMuAnalysis_2017_934V1/pellicci-ZEMuAnalysis_NANOAOD_2017_10218V2-df769e3b6a68f1e897c86e71b2345849/USER'
    # p = Process(target=submit, args=(config,))
    # p.start()
    # p.join()

    ################### 2018 Samples #########################

    # config.JobType.scriptArgs = ['isData=MC','year=2018']
    # config.General.workArea = 'crab_projects/samples_MC_2018/'
    # config.General.requestName = '2018_ZEMuAnalysis_Signal'
    # config.Data.inputDataset = '/ZEMuAnalysis_10218V2/pellicci-ZEMuAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER'
    # p = Process(target=submit, args=(config,))
    # p.start()
    # p.join()

    # config.JobType.scriptArgs = ['isData=MC','year=2018']
    # config.General.workArea = 'crab_projects/samples_MC_2018/'
    # config.General.requestName = '2018_LFVAnalysis_HEMu'
    # config.Data.inputDataset = '/LFVAnalysis_HEMu_2018_10218V1/mimacken-LFVAnalysis_NANOAOD_8028V1-99b0758841467aa49bae030484c7d875/USER'
    # p = Process(target=submit, args=(config,))
    # p.start()
    # p.join()
