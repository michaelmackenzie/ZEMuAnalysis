import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra):
        self.runningEra = runningEra
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("M_ll",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        PuppiMET = Object(event, "PuppiMET")

        minmupt = 25.
        minelept = 28.
        if self.runningEra == 2 :
            minelept = 33.


        if PuppiMET.pt > 50. :
            return False

        if runningEra == 0 :
            if not (HLT.IsoMu24 or HLT.Mu50 or HLT.Ele27_WPTight_Gsf) :
                return False

        elif runningEra == 1 :
            if not (HLT.IsoMu27 or HLT.Mu50 or HLT.Ele32_WPTight_Gsf or HLT.Ele32_WPTight_Gsf_L1DoubleEG) :
                return False

        elif runningEra == 2 :
            if not (HLT.IsoMu24 or HLT.Mu50 or HLT.Ele32_WPTight_Gsf) :
                return False

        if (len(electrons) + len(muons) != 2) :
            return False

        if len(muons) == 2 :
            lep_mass = (muons[0].p4() + muons[1].p4()).M() 
            if (lep_mass < 70. or lep_mass > 110.) :
                return False
            if ( muons[0].charge * muons[1].charge > 0 ) :
                return False
            if not muons[0].tightId :
                return False
            if not muons[1].tightId :
                return False
            if muons[0].pfRelIso03_all > 0.2 or muons[1].pfRelIso03_all > 0.2 : #medium
                return False
            if muons[0].pt < minmupt or muons[1].pt < minmupt :
                return False

        elif len(electrons) == 2 :
            lep_mass = (electrons[0].p4() + electrons[1].p4()).M()
            if (lep_mass < 70. or lep_mass > 110.) :
                return False
            if ( electrons[0].charge * electrons[1].charge > 0 ) :
                return False
            if not electrons[0].mvaFall17V2Iso_WP80 :
                return False
            if not electrons[1].mvaFall17V2Iso_WP80 :
                return False

            if electrons[0].pt < minelept or electrons[1].pt < minelept :
                    return False

        else :
            lep_mass = (muons[0].p4() + electrons[0].p4()).M()
            if (lep_mass < 70. or lep_mass > 110.) :
                return False
            if ( muons[0].charge * electrons[0].charge > 0 ) :
                return False
            if not muons[0].tightId :
                return False
            if muons[0].pfRelIso03_all > 0.2 : #medium
                return False
            if not electrons[0].mvaFall17V2Iso_WP80 :
                return False
            if muons[0].pt < minelept or electrons[0].pt < minelept :
                return False

        nbjets_25 = 0
        jetptmax = -1.
        for jetcount in xrange(len(jets)) :
            pt_of_jet = jets[jetcount].pt
            if pt_of_jet > jetptmax :
                jetptmax = pt_of_jet
            if pt_of_jet > 25. and jets[jetcount].btagDeepB > 0.4184 :   #medium
                nbjets_25 = nbjets_25 + 1
        if nbjets_25 > 0 or jetptmax > 100.:
            return False

        #it it's the same flavor channel, just save the full selection to spare space and CPU
        if len(muons) == 2 or len(electrons) == 2 :
            if jetptmax > 78 or PuppiMET.pt > 28. :
                return False


        self.out.fillBranch("M_ll",lep_mass)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra : exampleProducer(runningEra)
