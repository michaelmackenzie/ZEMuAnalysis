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


    config.JobType.scriptArgs = ['isData=MC','year=2016']
    config.General.workArea = 'crab_projects/samples_MC_2016/'
    config.General.requestName = '2016_ZEMuAnalysis_Signal'
    config.Data.inputDataset = '/ZEMuAnalysis_2016_8028V1/pellicci-ZEMuAnalysis_NANOAOD_10218V1-b1c578360797952dfc156561d5f36519/USER'
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

    # config.JobType.scriptArgs = ['isData=MC','year=2017']
    # config.General.workArea = 'crab_projects/samples_MC_2017/'
    # config.General.requestName = '2017_ZEMuAnalysis_Signal'
    # config.Data.inputDataset = '/ZEMuAnalysis_2017_1064V1/pellicci-ZEMuAnalysis_NANOAOD_2017_1064V1-b8e5db6dc58e02fa065eca4e059912ff/USER'
    # p = Process(target=submit, args=(config,))
    # p.start()
    # p.join()

    # config.JobType.scriptArgs = ['isData=MC','year=2018']
    # config.General.workArea = 'crab_projects/samples_MC_2018/'
    # config.General.requestName = '2018_ZEMuAnalysis_Signal'
    # config.Data.inputDataset = '/ZEMuAnalysis_10218V2/pellicci-ZEMuAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER'
    # p = Process(target=submit, args=(config,))
    # p.start()
    # p.join()
