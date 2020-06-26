import ROOT
import math

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
        self.out.branch("M_ll" ,  "F"); # di-lepton mass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        PuppiMET = Object(event, "PuppiMET")

        # sparsing parameters
        minmupt     = 25.
        minmuptlow  = 10. # for electron trigger
        minelept    = 33.
        mineleptlow = 15. # for muon trigger
        jetIdflag   = 4
        jetPUIdflag = 6
        maxMET      = 50.
        maxJetPt    = -1. # < 0 to apply no cut
        minLepM     = 75.
        maxLepM     = 160.
        cutBJets    = False
        muonIso     = 0.15 #tight ID
        
        # selection parameters
        maxJetPt_s = 78.
        maxMET_s   = 28.
        
        if self.runningEra == 0 :
            jetIdflag = 7 #different flag for 2016
            minelept = 28. #lower pT trigger
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT trigger

        if PuppiMET.pt > maxMET : #cut high MET events
            return False

        muonTriggered = False
        electronTriggered = False
        if self.runningEra == 0 :
            if HLT.IsoMu24 or HLT.Mu50 :
                muonTriggered = True
            if HLT.Ele27_WPTight_Gsf :
                electronTriggered = True
        elif self.runningEra == 1 :
            if HLT.IsoMu27 or HLT.Mu50 :
                muonTriggered = True
            if HLT.Ele32_WPTight_Gsf_L1DoubleEG :
                electronTriggered = True
        elif self.runningEra == 2 :
            if HLT.IsoMu24 or HLT.Mu50 :
                muonTriggered = True
            if HLT.Ele32_WPTight_Gsf :
                electronTriggered = True

        #require a trigger
        if not muonTriggered and not electronTriggered :
            return False

        #ee, mumu, or emu only
        if (len(electrons) + len(muons) != 2) :
            return False

        if len(muons) == 2 :
            if not muonTriggered:
                return False
            lep_mass = (muons[0].p4() + muons[1].p4()).M() 
            if (lep_mass < minLepM or lep_mass > maxLepM) :
                return False
            if ( muons[0].charge * muons[1].charge > 0 ) :
                return False
            if not muons[0].tightId :
                return False
            if not muons[1].tightId :
                return False
            if muons[0].pfRelIso04_all > muonIso or muons[1].pfRelIso04_all > muonIso :
                return False
            if muons[0].pt < minmupt or muons[1].pt < minmupt :
                return False

        elif len(electrons) == 2 :
            if not electronTriggered :
                return False
            lep_mass = (electrons[0].p4() + electrons[1].p4()).M()
            if (lep_mass < minLepM or lep_mass > maxLepM) :
                return False
            if ( electrons[0].charge * electrons[1].charge > 0 ) :
                return False
            if not electrons[0].mvaFall17V2Iso_WP80 :
                return False
            if not electrons[1].mvaFall17V2Iso_WP80 :
                return False
            if math.fabs(electrons[0].eta + electrons[0].deltaEtaSC) > 1.442 and math.fabs(electrons[0].eta + electrons[0].deltaEtaSC) < 1.566 :
                return False

            if math.fabs(electrons[1].eta + electrons[1].deltaEtaSC) > 1.442 and math.fabs(electrons[1].eta + electrons[1].deltaEtaSC) < 1.566 :
                return False

            if electrons[0].pt < minelept or electrons[1].pt < minelept :
                return False

        else :
            lep_mass = (muons[0].p4() + electrons[0].p4()).M()
            if (lep_mass < minLepM or lep_mass > maxLepM) :
                return False
            if ( muons[0].charge * electrons[0].charge > 0 ) :
                return False
            if not muons[0].tightId :
                return False
            if muons[0].pfRelIso04_all > muonIso :
                return False
            if not electrons[0].mvaFall17V2Iso_WP80 :
                return False

            if math.fabs(electrons[0].eta + electrons[0].deltaEtaSC) > 1.442 and math.fabs(electrons[0].eta + electrons[0].deltaEtaSC) < 1.566 :
                return False
            #check triggers with threshold on triggering lepton
            if not ((muonTriggered and muons[0].pt > minmupt) or (electronTriggered and electrons[0].pt > minelept)) :
                return False
            #check objects pass thresholds
            if muons[0].pt < minmuptlow or electrons[0].pt < mineleptlow :
                return False

        jetptmax  = -1.
        for jetcount in xrange(len(jets)) :
            if jets[jetcount].jetId < jetIdflag :
                continue
            pt_of_jet = jets[jetcount].pt
            if pt_of_jet < 50. and jets[jetcount].puId < jetPUIdflag :
                continue

            if pt_of_jet > jetptmax :
                jetptmax = pt_of_jet
                if maxJetPt > 0. and jetptmax > maxJetPt :
                    return False
            if cutBJets and pt_of_jet > 25. and jets[jetcount].btagDeepB > 0.4184 :   #medium
                return False

        #if it's the same flavor channel, just save the full selection to spare space and CPU
        if len(muons) == 2 or len(electrons) == 2 :
            if jetptmax > maxJetPt_s or PuppiMET.pt > maxMET_s :
                return False


        self.out.fillBranch("M_ll", lep_mass)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra : exampleProducer(runningEra)
