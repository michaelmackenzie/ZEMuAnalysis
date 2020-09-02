import ROOT
import math

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra):
        self.runningEra = runningEra
        self.seen = 0
        self.mutau = 0
        self.etau = 0
        self.emu = 0
        self.mumu = 0
        self.ee = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        print "Saw", self.emu, "e+mu,", self.etau,"e+tau,", self.mutau, "mu+tau,", self.mumu, "mu+mu, and", self.ee, "ee"
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("M_ll" ,  "F"); # di-lepton mass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        verbose = 1
        self.seen = self.seen + 1
        
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT       = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        taus      = Collection(event, "Tau")
        jets      = Collection(event, "Jet")
        PuppiMET  = Object(event, "PuppiMET")

        ## trigger parameter ##
        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT trigger in 2017

        ## Non-trigger lepton parameters ##
        minmuptlow  = 5.
        mineleptlow = 10.
        mintaupt = 20.
        
        ## jet parameters ##
        jetIdflag   = 4
        jetPUIdflag = 6
        if self.runningEra == 0:
            jetIdflag = 7 #different flag for 2016


        ## muon isolation cut levels ##
        muonIsoVLoose  = 0.4
        muonIsoLoose   = 0.25 #eff ~ 0.98
        muonIsoMedium  = 0.20
        muonIsoTight   = 0.15 #eff ~ 0.95
        muonIsoVTight  = 0.10
        muonIsoVVTight = 0.05

        ## selection parameters ##
        maxMET      = -1. # < 0 to apply no cut
        maxJetPt    = -1. # < 0 to apply no cut
        minLepM     = 45. # generator only went down to 50 GeV/c^2
        maxLepM     = 170.
        cutBJets    = False

        # switch between tau IDs (deep NN IDs or old MVA IDs)
        useDeepNNTauIDs = True
        
        muonIso    = muonIsoTight
        tauAntiEle = 7 # (bitmask) MVA: 8 = tight, 16 = very tight deepNN:  1 = VVVLoose 2 = VVLoose 4 = VLoose   8 = Loose
        #                                                                  16 = Medium  32 = Tight  64 = VTight 128 = VVTight
        tauAntiMu  = 1 # (bitmask) MVA: 1 = loose 2 = tight deepNN: 1 = VLoose 2 = Loose 4 = Medium 8 = Tight
        tauAntiJet = 7 # (bitmask) deepNN: 1 = VVVLoose 2 = VVLoose 4 = VLoose 8 = Loose 16 = Medium 32 = Tight 64 = VTight 128 = VVTight
        tauIso     = 7 
        tauDeltaR  = 0.3
        
        ## counting veto parameters ##
        doCountingSelection = True # else just use length of the array
        # muons
        minmupt_count = 0. # 3 GeV/c threshold in nanoAOD
        muonIso_count = muonIsoVLoose
        muonId_count = 1 # 1 = loose, 2 = medium, 3 = tight
        # electrons
        minelept_count = 0. # 5 GeV/c threshold in nanoAOD
        eleId_count = 1 #0 = none 1 = WPL, 2 = WP80, 3 = WP90
        # taus
        mintaupt_count = 20.
        tauAntiEle_count = 2
        tauAntiMu_count = 2
        tauAntiJet_count = 4
        tauIso_count = 0
        tauIdDecay_count = False
        tauDeltaR_count = 0.3 #distance from selected electrons/muons
        

        ### initial filtering ###
        if maxMET > 0 and PuppiMET.pt > maxMET : #cut high MET events
            return False


        ################ count objects ####################
        nElectrons = 0
        nMuons = 0
        nTaus = 0
        elec_dict = dict() # save a dictionary to find the objects again
        muon_dict = dict()
        tau_dict = dict()
        if doCountingSelection :
            for index in range(len(electrons)) :
                if(verbose > 9 and self.seen % 10 == 0):
                    print "Electron", index, "pt =", electrons[index].pt, "WPL =", electrons[index].mvaFall17V2Iso_WPL, "WP80 =", electrons[index].mvaFall17V2Iso_WP80 
                if (electrons[index].pt > minelept_count and
                    ( eleId_count == 0 or
                     (eleId_count == 1 and electrons[index].mvaFall17V2Iso_WPL ) or
                     (eleId_count == 2 and electrons[index].mvaFall17V2Iso_WP80) or
                     (eleId_count == 3 and electrons[index].mvaFall17V2Iso_WP90))) :
                    elec_dict[nElectrons] = electrons[index]
                    nElectrons = nElectrons + 1
            for index in range(len(muons)) :
                if(verbose > 9 and self.seen % 10 == 0):
                    print "Muon", index, "pt =", muons[index].pt, "IDL =", muons[index].looseId, "IDM =", muons[index].tightId, "IDT =", muons[index].tightId, "iso = ", muons[index].pfRelIso04_all 
                if (muons[index].pt > minmupt_count and
                    ((muonId_count == 1 and muons[index].looseId) or
                     (muonId_count == 2 and muons[index].mediumId) or
                     (muonId_count == 3 and muons[index].tightId)) and
                    muons[index].pfRelIso04_all < muonIso_count) :
                    muon_dict[nMuons] = muons[index]
                    nMuons = nMuons + 1
            for index in range(len(taus)) :
                if(verbose > 9 and self.seen % 10 == 0):
                    print "Tau", index, "pt =", taus[index].pt, "AntiMu =", taus[index].idDeepTau2017v2p1VSmu, "AntiEle =", taus[index].idDeepTau2017v2p1VSe, "AntiJet =", taus[index].idDeepTau2017v2p1VSjet
                if taus[index].pt > mintaupt_count and abs(taus[index].eta) < 2.3:
                    if ((useDeepNNTauIDs and
                         taus[index].idDeepTau2017v2p1VSe >= tauAntiEle_count and
                         taus[index].idDeepTau2017v2p1VSmu >= tauAntiMu_count and
                         taus[index].idDeepTau2017v2p1VSjet >= tauAntiJet_count and
                         (taus[index].idDecayModeNewDMs or not tauIdDecay_count))
                        or (not useDeepNNTauIDs and
                            taus[index].idAntiEle >= tauAntiEle_count and
                            taus[index].idAntiMu >= tauAntiMu_count and
                            taus[index].idMVAnewDM2017v2 >= tauIso_count and
                            (taus[index].idDecayMode or not tauIdDecay_count))) :
                        deltaRCheck = True
                        if tauDeltaR_count > 0:
                            for i_elec in range(nElectrons):
                                deltaRCheck = deltaRCheck and taus[index].p4().DeltaR(elec_dict[i_elec].p4()) > tauDeltaR_count
                                if not deltaRCheck:
                                    break
                            for i_muon in range(nMuons):
                                if not deltaRCheck:
                                    break
                                deltaRCheck = deltaRCheck or taus[index].p4().DeltaR(muon_dict[i_muon]) > tauDeltaR_count
                        if deltaRCheck:
                            tau_dict[nTaus] = taus[index]
                            nTaus = nTaus + 1
        else :
            nElectrons = len(electrons)
            nMuons     = len(muons)
            nTaus      = len(taus)

        if (verbose > 1 and self.seen % 100 == 0) or (verbose > 2 and self.seen % 10 == 0):
            print "seen",self.seen,"ntau (len) =",nTaus,"(", len(taus),") nelectron (len) =",nElectrons,"(", len(electrons),") nmuon (len) =",nMuons,"(",len(muons),") met =",PuppiMET.pt

        ### filter events that can't pass selections ###
        if nElectrons == 1 and nMuons == 0 and nTaus != 1: #etau
            return False
        if nElectrons == 0 and nMuons == 1 and nTaus != 1: #mutau
            return False
        if nTaus == 0 and nElectrons + nMuons > 2: #ee, emu, mumu
            return False

        ## check which triggers are fired ##
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
            if HLT.Ele32_WPTight_Gsf_L1DoubleEG and HLT.Ele35_WPTight_GsF_L1EGMT : #seems to be recommended to use L1 seed of HLT_Ele35 as well
                electronTriggered = True
        elif self.runningEra == 2 :
            if HLT.IsoMu24 or HLT.Mu50 :
                muonTriggered = True
            if HLT.Ele32_WPTight_Gsf :
                electronTriggered = True
        if (verbose > 1 and self.seen % 100 == 0) or (verbose > 2 and self.seen % 10 == 0):
            print "muonTriggered =",muonTriggered,"electronTriggered =",electronTriggered
        #require a trigger
        if not muonTriggered and not electronTriggered :
            return False

        ## check if the event passes each selection ##
        mutau = False
        etau  = False
        emu   = False
        ee    = False
        mumu  = False
        # mutau
        if nMuons == 1 and nTaus == 1:
            if doCountingSelection :
                lep1 = muon_dict[0]
                lep2 = tau_dict[0]
            else :
                lep1 = muons[0]
                lep2 = taus[0]
            mutau = lep1.tightId and lep1.pfRelIso04_all < muonIso and lep1.pt > minmupt and lep2.pt > mintaupt
            if useDeepNNTauIDs:
                mutau = mutau and lep2.idDeepTau2017v2p1VSe >= tauAntiEle
                mutau = mutau and lep2.idDeepTau2017v2p1VSmu >= tauAntiMu
                mutau = mutau and lep2.idDeepTau2017v2p1VSjet >= tauAntiJet
                mutau = mutau and lep2.idDecayModeNewDMs
            else:
                mutau = mutau and lep2.idAntiEle >= tauAntiEle
                mutau = mutau and lep2.idAntiMu >= tauAntiMu
                mutau = mutau and lep2.idMVAnewDM2017v2 >= tauIso
                mutau = mutau and lep2.idDecayMode
            mutau = mutau and lep1.p4().DeltaR(lep2.p4()) > tauDeltaR
        # etau
        if nElectrons == 1 and nTaus == 1:
            if doCountingSelection :
                lep1 = elec_dict[0]
                lep2 = tau_dict[0]
            else :
                lep1 = electrons[0]
                lep2 = taus[0]
            etau = lep1.mvaFall17V2Iso_WP80
            etau = etau and (math.fabs(lep1.eta + lep1.deltaEtaSC) < 1.442 or math.fabs(lep1.eta + lep1.deltaEtaSC) > 1.566) 
            etau = etau and lep1.pt > minelept and lep2.pt > mintaupt
            if useDeepNNTauIDs:
                etau = etau and lep2.idDeepTau2017v2p1VSe >= tauAntiEle
                etau = etau and lep2.idDeepTau2017v2p1VSmu >= tauAntiMu
                etau = etau and lep2.idDeepTau2017v2p1VSjet >= tauAntiJet
                etau = etau and lep2.idDecayModeNewDMs
            else:
                etau = etau and lep2.idAntiEle >= tauAntiEle
                etau = etau and lep2.idAntiMu >= tauAntiMu
                etau = etau and lep2.idMVAnewDM2017v2 >= tauIso
                etau = etau and lep2.idDecayMode
            etau = etau and lep1.p4().DeltaR(lep2.p4()) > tauDeltaR
        # veto from tau categories if passes both (good looking e, mu, and tau)
        if mutau and etau:
            mutau = False
            etau  = False
        # emu
        if nElectrons == 1 and nMuons == 1:
            if doCountingSelection :
                lep1 = elec_dict[0]
                lep2 = muon_dict[0]
            else :
                lep1 = electrons[0]
                lep2 = muons[0]
            emu =  lep2.tightId and lep2.pfRelIso04_all < muonIso and lep1.mvaFall17V2Iso_WP80
            emu = emu and (math.fabs(lep1.eta + lep1.deltaEtaSC) < 1.442 or math.fabs(lep1.eta + lep1.deltaEtaSC) > 1.566)
            emu = emu and lep1.pt > mineleptlow and lep2.pt > minmuptlow
        # mumu
        elif nMuons == 2 and not (mutau or etau):
            if doCountingSelection :
                lep1 = muon_dict[0]
                lep2 = muon_dict[1]
            else :
                lep1 = muons[0]
                lep2 = muons[1]
            mumu = lep1.tightId and lep2.tightId
            mumu = mumu and lep1.pfRelIso04_all < muonIso and lep2.pfRelIso04_all < muonIso
            mumu = mumu and (lep1.pt > minmupt or lep2.pt > minmupt)
            mumu = mumu and lep1.pt > minmuptlow and lep2.pt > minmuptlow
        # ee
        elif nElectrons == 2 and not (mutau or etau):
            if doCountingSelection :
                lep1 = elec_dict[0]
                lep2 = elec_dict[1]
            else :
                lep1 = electrons[0]
                lep2 = electrons[1]
            ee = lep1.mvaFall17V2Iso_WP80 and lep2.mvaFall17V2Iso_WP80
            ee = ee and (math.fabs(lep1.eta + lep1.deltaEtaSC) < 1.442 or math.fabs(lep1.eta + lep1.deltaEtaSC) > 1.566)
            ee = ee and (math.fabs(lep2.eta + lep2.deltaEtaSC) < 1.442 or math.fabs(lep2.eta + lep2.deltaEtaSC) > 1.566)
            ee = ee and (lep1.pt > minelept or lep2.pt > minelept)
            ee = ee and lep1.pt > mineleptlow and lep2.pt > mineleptlow

        # overlap shouldn't happen, but remove if it somehow does
        if emu and (mutau or etau):
            mutau = False
            etau = False
            
        # must pass a selection
        if not (mutau or etau or emu or mumu or ee):
            return False


        ## Filter by mass range ##
        # lep1 and lep2 should still be properly set from selection checks
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
            return False

        ## check proper trigger is fired ##
        if mumu :
            if not muonTriggered:
                return False
        elif ee :
            if not electronTriggered :
                return False
        elif mutau :
            if not muonTriggered:
                return False
        elif etau :
            if not electronTriggered :
                return False
        elif emu:
            #check triggers with threshold on triggering lepton
            if not ((muonTriggered and lep2.pt > minmupt) or (electronTriggered and lep1.pt > minelept)) :
                return False

        else :
            print "ERROR! No selection found!"
            return False

        ## cut events with high pT jets (reduce top backgrounds) ##
        if maxJetPt > 0.:
            jetptmax  = -1.
            for jetcount in xrange(len(jets)) :
                if jets[jetcount].jetId < jetIdflag :
                    continue
                pt_of_jet = jets[jetcount].pt
                if pt_of_jet < 50. and jets[jetcount].puId < jetPUIdflag :
                    continue

                if pt_of_jet > jetptmax :
                    jetptmax = pt_of_jet
                    if jetptmax > maxJetPt :
                        return False
                if cutBJets and pt_of_jet > 25. and jets[jetcount].btagDeepB > 0.4184 :   #medium
                    return False

        if (verbose > 1 and self.seen % 100 == 0) or (verbose > 2 and self.seen % 10 == 0):
            print "passing event."

        self.out.fillBranch("M_ll", lep_mass)

        # increment selection counts
        if emu:
            self.emu = self.emu+1
        elif etau:
            self.etau = self.etau+1
        elif mutau:
            self.mutau = self.mutau+1
        elif mumu:
            self.mumu = self.mumu+1
        elif ee:
            self.ee = self.ee+1
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra : exampleProducer(runningEra)
