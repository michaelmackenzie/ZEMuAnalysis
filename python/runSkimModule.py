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
        self.isDY = False
        self.verbose = 1
        pass
    def beginJob(self):
        pass
    def endJob(self):
        print "Saw", self.emu, "e+mu,", self.etau,"e+tau,", self.mutau, "mu+tau,", self.mumu, "mu+mu, and", self.ee, "ee"
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("M_ll" ,  "F"); # di-lepton mass
        self.out.branch("leptonOneFlavor",  "I"); # lepton one flavor
        self.out.branch("leptonOneIndex" ,  "I"); # lepton one index
        self.out.branch("leptonTwoFlavor",  "I"); # lepton two flavor
        self.out.branch("leptonTwoIndex" ,  "I"); # lepton two index
        self.out.branch("zPt"            ,  "F"); # Gen-level Z pT
        self.out.branch("zMass"          ,  "F"); # Gen-level Z mass
        self.out.branch("zLepOne"        ,  "I"); # Gen-level Z lepton daughter 1
        self.out.branch("zLepTwo"        ,  "I"); # Gen-level Z lepton daughter 1
        name = inputFile.GetName()
        # data samples from Z to ll (include LFV just for Z info)
        self.isDY = ("DYJetsToLL" in name) or ("ZMuTau" in name) or ("ZETau" in name) or ("ZEMu" in name)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    # get generator info for Z boson
    def genZInfo(self, event):
        genParts = Collection(event, "GenPart")
        ngenpart = len(genParts)
        zpt = -1.
        zmass = -1.
        leponeid = 0
        leptwoid = 0
        for index in range(ngenpart):
            if genParts[index].pdgId == 23: #z boson
                if (genParts[index].statusFlags & (1<<13)): #check if isLastCopy()
                    zpt = genParts[index].pt
                    zmass = genParts[index].mass
                else : #save values in case no Z passes the last copy check, if not filled already
                    if zpt < 0. :
                        zpt = genParts[index].pt
                    if zmass < 0. :
                        zmass = genParts[index].mass
            elif ((abs(genParts[index].pdgId) == 11 or abs(genParts[index].pdgId) == 13 or abs(genParts[index].pdgId) == 15) #charged lepton
                  and genParts[index].genPartIdxMother >= 0 and genParts[genParts[index].genPartIdxMother].pdgId == 23): #parent is z-boson
                if leponeid == 0:
                    leponeid = genParts[index].pdgId
                else:
                    leptwoid = genParts[index].pdgId
        if zpt < 0. or zmass < 0. or leponeid == 0 or leptwoid == 0:
            print "Warning! Not all Z information was found in event", self.seen
            print "Found Z pT =", zpt, "and Mass =", zmass, ". Lep One Pdg ID =", leponeid, "and Lep Two Pdg ID =", leptwoid
            print "Attempting to replace the Z by looking for two leptons with parent = 0..."
            if self.verbose > 1:
                print "Printing the gen particle information:"
            leponeindex = -1
            leptwoindex = -1
            for index in range(ngenpart):
                if self.verbose > 1:
                    print "Index", index, ": Pdg =", genParts[index].pdgId, " parent =", genParts[index].genPartIdxMother, \
                        "mass =", genParts[index].mass, "pt =", genParts[index].pt
                if((abs(genParts[index].pdgId) == 11 or abs(genParts[index].pdgId) == 13 or abs(genParts[index].pdgId) == 15) #charged lepton
                   and genParts[index].genPartIdxMother == 0) : #Mother is original quark
                    if leponeindex < 0:
                        leponeindex = index
                    elif leptwoindex < 0:
                        leptwoindex = index
            if leponeindex < 0 or leptwoindex < 0:
                print "Failed to find leptons coming from particle 0!"
            else :
                lv1 = ROOT.TLorentzVector()
                lv1.SetPtEtaPhiM(genParts[leponeindex].pt, genParts[leponeindex].eta, genParts[leponeindex].phi, genParts[leponeindex].mass)
                lv2 = ROOT.TLorentzVector()
                lv2.SetPtEtaPhiM(genParts[leptwoindex].pt, genParts[leptwoindex].eta, genParts[leptwoindex].phi, genParts[leptwoindex].mass)
                zpt = (lv1+lv2).Pt()
                zmass = (lv1+lv2).M()
                leponeid = genParts[leponeindex].pdgId
                leptwoid = genParts[leptwoindex].pdgId
        self.out.fillBranch("zPt", zpt)
        self.out.fillBranch("zMass", zmass)
        self.out.fillBranch("zLepOne", leponeid)
        self.out.fillBranch("zLepTwo", leptwoid)
                
    def analyze(self, event):
        ############################
        #     Begin event loop     #
        ############################

        self.seen = self.seen + 1
        
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT       = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        taus      = Collection(event, "Tau")
        jets      = Collection(event, "Jet")
        PuppiMET  = Object(event, "PuppiMET")

        ############################
        #    Trigger parameters    #
        ############################

        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT electron trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT muon trigger in 2017

        ## Non-trigger lepton parameters ##
        minmuptlow  = 5.
        mineleptlow = 10.
        mintaupt = 20.

        ############################
        #       Object IDs         #
        ############################
        
        ## jet parameters ##
        jetIdflag   = 1
        jetPUIdflag = 4


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
        minLepM     = 50. # generator only went down to 50 GeV/c^2
        maxLepM     = 170.
        cutBJets    = False

        # switch between tau IDs (deep NN IDs or old MVA IDs)
        useDeepNNTauIDs = True
        
        muonIso    = muonIsoTight
        tauAntiEle = 1 # (bitmask) MVA: 8 = tight, 16 = very tight deepNN:  1 = VVVLoose 2 = VVLoose 4 = VLoose   8 = Loose
        #                                                                  16 = Medium  32 = Tight  64 = VTight 128 = VVTight
        tauAntiEle_etau = 50 #higher veto requirement for ee -> e fake tau
        tauAntiMu  = 10 # (bitmask) MVA: 1 = loose 2 = tight deepNN: 1 = VLoose 2 = Loose 4 = Medium 8 = Tight
        tauAntiJet = 50 # (bitmask) deepNN: 1 = VVVLoose 2 = VVLoose 4 = VLoose 8 = Loose 16 = Medium 32 = Tight 64 = VTight 128 = VVTight
        tauIso     = 7 
        tauDeltaR  = 0.3

        ############################
        #     Veto object IDs      #
        ############################
        
        ## counting veto parameters ##
        doCountingSelection = True # else just use length of the array
        # muons
        minmupt_count = 5. # 3 GeV/c threshold in nanoAOD
        muonIso_count = muonIsoVLoose
        muonId_count = 1 # 1 = loose, 2 = medium, 3 = tight
        # electrons
        minelept_count = 10. # 5 GeV/c threshold in nanoAOD
        eleId_count = 1 #0 = none 1 = WPL, 2 = WP80, 3 = WP90        
        # taus
        mintaupt_count = 20.
        tauAntiEle_count = 1
        tauAntiMu_count = 10
        tauAntiJet_count = 50
        tauIso_count = 0
        tauIdDecay_count = True
        tauDeltaR_count = 0.3 #distance from selected electrons/muons
        

        ############################
        #     Begin selections     #
        ############################
        
        ### initial filtering ###
        if maxMET > 0 and PuppiMET.pt > maxMET : #cut high MET events
            return False

        ############################
        #    Trigger selection     #
        ############################
        ### check which triggers are fired ###
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
            if HLT.Ele32_WPTight_Gsf_L1DoubleEG: # and HLT.Ele35_WPTight_GsF_L1EGMT : FIXME #seems to be recommended to use L1 seed of HLT_Ele35 as well
                electronTriggered = True
        elif self.runningEra == 2 :
            if HLT.IsoMu24 or HLT.Mu50 :
                muonTriggered = True
            if HLT.Ele32_WPTight_Gsf :
                electronTriggered = True
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0):
            print "muonTriggered =",muonTriggered,"electronTriggered =",electronTriggered
        #require a trigger
        if not muonTriggered and not electronTriggered :
            return False

        ############################
        #      Count leptons       #
        ############################

        nElectrons = 0
        nMuons = 0
        nTaus = 0
        elec_dict = dict() # save a dictionary to find the objects again
        muon_dict = dict()
        tau_dict = dict()
        if doCountingSelection :
            ############################
            #     Count electrons      #
            ############################
            for index in range(len(electrons)) :
                if(self.verbose > 9 and self.seen % 10 == 0):
                    print "Electron", index, "pt =", electrons[index].pt, "WPL =", electrons[index].mvaFall17V2Iso_WPL, \
                        "WP80 =", electrons[index].mvaFall17V2Iso_WP80 
                if (electrons[index].pt > minelept_count and
                    ( eleId_count == 0 or
                     (eleId_count == 1 and electrons[index].mvaFall17V2Iso_WPL ) or
                     (eleId_count == 2 and electrons[index].mvaFall17V2Iso_WP80) or
                     (eleId_count == 3 and electrons[index].mvaFall17V2Iso_WP90))) :
                    elec_dict[nElectrons] = index
                    nElectrons = nElectrons + 1
            ############################
            #       Count muons        #
            ############################
            for index in range(len(muons)) :
                if(self.verbose > 9 and self.seen % 10 == 0):
                    print "Muon", index, "pt =", muons[index].pt, "IDL =", muons[index].looseId, "IDM =", muons[index].tightId, \
                        "IDT =", muons[index].tightId, "iso = ", muons[index].pfRelIso04_all 
                if (muons[index].pt > minmupt_count and
                    ((muonId_count == 1 and muons[index].looseId) or
                     (muonId_count == 2 and muons[index].mediumId) or
                     (muonId_count == 3 and muons[index].tightId)) and
                    muons[index].pfRelIso04_all < muonIso_count) :
                    muon_dict[nMuons] = index
                    nMuons = nMuons + 1
            ############################
            #       Count taus         #
            ############################
            for index in range(len(taus)) :
                if(self.verbose > 9 and self.seen % 10 == 0):
                    print "Tau", index, "pt =", taus[index].pt, "AntiMu =", taus[index].idDeepTau2017v2p1VSmu, "AntiEle =", \
                        taus[index].idDeepTau2017v2p1VSe, "AntiJet =", taus[index].idDeepTau2017v2p1VSjet
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
                        if tauDeltaR_count > 0: #check for overlap with accepted lepton
                            for i_elec in range(nElectrons):
                                deltaRCheck = deltaRCheck and taus[index].p4().DeltaR(electrons[elec_dict[i_elec]].p4()) > tauDeltaR_count
                                if not deltaRCheck:
                                    break
                            for i_muon in range(nMuons):
                                deltaRCheck = deltaRCheck and taus[index].p4().DeltaR(muons[muon_dict[i_muon]].p4()) > tauDeltaR_count
                                if not deltaRCheck:
                                    break
                        if deltaRCheck:
                            tau_dict[nTaus] = index
                            nTaus = nTaus + 1
        else :
            nElectrons = len(electrons)
            nMuons     = len(muons)
            nTaus      = len(taus)

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0):
            print "seen",self.seen,"ntau (len) =",nTaus,"(", len(taus),") nelectron (len) =",nElectrons,"(", len(electrons),") nmuon (len) =",\
                nMuons,"(",len(muons),") met =",PuppiMET.pt

        ############################
        #  Filter by lepton count  #
        ############################
        if nElectrons + nMuons < 1: #nothing to trigger on
            return False
        if nElectrons + nMuons == 1 and nTaus != 1: #etau,mutau
            return False
        if nTaus == 0 and nElectrons + nMuons > 2: #ee, emu, mumu
            return False
        #no trigger-able leptons
        if nElectrons == 0 and not muonTriggered:
            return False
        if nMuons == 0 and not electronTriggered:
            return False

        ############################
        #   Check each selection   #
        ############################
        ## check if the event passes each selection ##
        mutau = False
        etau  = False
        emu   = False
        ee    = False
        mumu  = False

        ## store selected lepton info ##
        leptonOneIndex  = -1
        leptonOneFlavor = 0
        leptonTwoIndex  = -1
        leptonTwoFlavor = 0
        
        ############################
        #          Mu+Tau          #
        ############################
        # mutau
        if nMuons == 1 and nTaus == 1:
            if doCountingSelection :
                leptonOneIndex = muon_dict[0]
                leptonTwoIndex = tau_dict[0]
                lep1 = muons[muon_dict[0]]
                lep2 = taus[tau_dict[0]]
            else :
                leptonOneIndex = 0
                leptonTwoIndex = 0
                lep1 = muons[0]
                lep2 = taus[0]
            leptonOneFlavor = lep1.charge*-13
            leptonTwoFlavor = lep2.charge*-15
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
        ############################
        #          E+Tau           #
        ############################
        if nElectrons == 1 and nTaus == 1:
            if doCountingSelection :
                leptonOneIndex = elec_dict[0]
                leptonTwoIndex = tau_dict[0]
                lep1 = electrons[elec_dict[0]]
                lep2 = taus[tau_dict[0]]
            else :
                leptonOneIndex = 0
                leptonTwoIndex = 0
                lep1 = electrons[0]
                lep2 = taus[0]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-15
            etau = lep1.mvaFall17V2Iso_WP80
            etau = etau and (math.fabs(lep1.eta + lep1.deltaEtaSC) < 1.442 or math.fabs(lep1.eta + lep1.deltaEtaSC) > 1.566) 
            etau = etau and lep1.pt > minelept and lep2.pt > mintaupt
            if useDeepNNTauIDs:
                etau = etau and lep2.idDeepTau2017v2p1VSe >= tauAntiEle_etau
                etau = etau and lep2.idDeepTau2017v2p1VSmu >= tauAntiMu
                etau = etau and lep2.idDeepTau2017v2p1VSjet >= tauAntiJet
                etau = etau and lep2.idDecayModeNewDMs
            else:
                etau = etau and lep2.idAntiEle >= tauAntiEle_etau
                etau = etau and lep2.idAntiMu >= tauAntiMu
                etau = etau and lep2.idMVAnewDM2017v2 >= tauIso
                etau = etau and lep2.idDecayMode
            etau = etau and lep1.p4().DeltaR(lep2.p4()) > tauDeltaR
        # veto from tau categories if passes both (good looking e, mu, and tau)
        if mutau and etau:
            mutau = False
            etau  = False
        ############################
        #           E+Mu           #
        ############################
        if nElectrons == 1 and nMuons == 1:
            if doCountingSelection :
                leptonOneIndex = elec_dict[0]
                leptonTwoIndex = muon_dict[0]
                lep1 = electrons[elec_dict[0]]
                lep2 = muons[muon_dict[0]]
            else :
                leptonOneIndex = 0
                leptonTwoIndex = 0
                lep1 = electrons[0]
                lep2 = muons[0]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-13
            emu =  lep2.tightId and lep2.pfRelIso04_all < muonIso and lep1.mvaFall17V2Iso_WP80
            emu = emu and (math.fabs(lep1.eta + lep1.deltaEtaSC) < 1.442 or math.fabs(lep1.eta + lep1.deltaEtaSC) > 1.566)
            emu = emu and lep1.pt > mineleptlow and lep2.pt > minmuptlow
        ############################
        #          Mu+Mu           #
        ############################
        elif nMuons == 2 and nElectrons == 0 and not (mutau or etau):
            if doCountingSelection :
                leptonOneIndex = muon_dict[0]
                leptonTwoIndex = muon_dict[1]
                lep1 = muons[muon_dict[0]]
                lep2 = muons[muon_dict[1]]
            else :
                leptonOneIndex = 0
                leptonTwoIndex = 1
                lep1 = muons[0]
                lep2 = muons[1]
            leptonOneFlavor = lep1.charge*-13
            leptonTwoFlavor = lep2.charge*-13
            mumu = lep1.tightId and lep2.tightId
            mumu = mumu and lep1.pfRelIso04_all < muonIso and lep2.pfRelIso04_all < muonIso
            mumu = mumu and (lep1.pt > minmupt or lep2.pt > minmupt)
            mumu = mumu and lep1.pt > minmuptlow and lep2.pt > minmuptlow
        ############################
        #           E+E            #
        ############################
        elif nElectrons == 2 and nMuons == 0 and not (mutau or etau):
            if doCountingSelection :
                leptonOneIndex = elec_dict[0]
                leptonTwoIndex = elec_dict[1]
                lep1 = electrons[elec_dict[0]]
                lep2 = electrons[elec_dict[1]]
            else :
                leptonOneIndex = 0
                leptonTwoIndex = 1
                lep1 = electrons[0]
                lep2 = electrons[1]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-11
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

        ############################
        #    Further filtering     #
        ############################

        ############################
        #     Mass filtering       #
        ############################
        ## Filter by mass range ##
        # lep1 and lep2 should still be properly set from selection checks
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
            return False

        ############################
        #    Trigger filtering     #
        ############################
        ## check proper trigger is fired ##
        muonLowTrig = False
        if self.runningEra == 0 or self.runningEra == 2 :
            muonLowTrig = HLT.IsoMu24
        elif self.runningEra == 1 :
            muonLowTrig = HLT.IsoMu27

        if mumu :
            if not muonTriggered:
                return False
            if not muonLowTrig : #only passed high pt trigger
                if not (lep1.pt > 50 or lep2.pt > 50.) :
                    return False                
        elif ee :
            if not electronTriggered :
                return False
        elif mutau :
            if not muonTriggered:
                return False
            if not muonLowTrig : #only passed high pt trigger
                if not (lep1.pt > 50) :
                    return False                
        elif etau :
            if not electronTriggered :
                return False
        elif emu:
            #check triggers with threshold on triggering lepton
            if not ((muonTriggered and lep2.pt > minmupt) or (electronTriggered and lep1.pt > minelept)) :
                return False
            if not muonLowTrig and not (electronTriggered and lep1.pt > minelept)  : #only passed high pt muon trigger
                if not (lep2.pt > 50) :
                    return False                

        else :
            print "ERROR! No selection found!"
            return False

        ############################
        #     B-Jet filtering      #
        ############################

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

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0):
            print "passing event."

        ############################
        #      Accept event        #
        ############################

        # Fill outgoing branches
        self.out.fillBranch("M_ll", lep_mass)
        self.out.fillBranch("leptonOneFlavor", leptonOneFlavor)
        self.out.fillBranch("leptonOneIndex" , leptonOneIndex)
        self.out.fillBranch("leptonTwoFlavor", leptonTwoFlavor)
        self.out.fillBranch("leptonTwoIndex" , leptonTwoIndex)
        # if DY event, fill extra info
        if(self.isDY):
            self.genZInfo(event)

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
