import ROOT
import math

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra, maxEvents, startEvent, isData, saveZ):
        self.runningEra = runningEra
        self.maxEvents = maxEvents #for quick local testing
        self.startEvent = startEvent
        self.isData = isData
        self.isDY = saveZ
        self.seen = 0
        self.mutau = 0
        self.etau = 0
        self.emu = 0
        self.mumu = 0
        self.ee = 0
        self.failTrigMap = 0
        self.negativeEvents = 0
        if self.maxEvents == 1:
            self.verbose = 20
        elif self.maxEvents > 0 and self.maxEvents < 10:
            self.verbose = 10
        elif self.maxEvents > 0:
            self.verbose = 2
        else:
            self.verbose = 1
        pass
    def beginJob(self):
        pass
    def endJob(self):
        print "Saw", self.emu, "e+mu,", self.etau,"e+tau,", self.mutau, "mu+tau,", self.mumu, "mu+mu, and", self.ee, "ee","from",(self.seen-self.startEvent+1),"events processed"
        print "Found", self.failTrigMap, "events that failed trigger matching requirements"
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
        self.out.branch("muonLowTrigger" ,  "O"); # fired muon low trigger
        self.out.branch("muonHighTrigger",  "O"); # fired muon high trigger
        self.out.branch("electronTrigger",  "O"); # fired electron trigger
        name = inputFile.GetName()
        # data samples from Z to ll (include LFV just for Z info)
        # self.isDY = self.isDY or ("DYJetsToLL" in name) or ("ZMuTau" in name) or ("ZETau" in name) or ("ZEMu" in name)
        print "Using isDY =", self.isDY
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        h = ROOT.TH1D("events", "events", 10, 1, 11)
        h.Fill(1.5, self.seen)
        h.Fill(2.5, self.emu)
        h.Fill(3.5, self.etau)
        h.Fill(4.5, self.mutau)
        h.Fill(5.5, self.mumu)
        h.Fill(6.5, self.ee)
        h.Fill(10.5, self.negativeEvents)
        h.Write()
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
            elif genParts[index].pdgId == 25: #h boson
                if (genParts[index].statusFlags & (1<<13)): #check if isLastCopy()
                    zpt = genParts[index].pt
                    zmass = genParts[index].mass
                else : #save values in case no H passes the last copy check, if not filled already
                    if zpt < 0. :
                        zpt = genParts[index].pt
                    if zmass < 0. :
                        zmass = genParts[index].mass
            elif ((abs(genParts[index].pdgId) == 11 or abs(genParts[index].pdgId) == 13 or abs(genParts[index].pdgId) == 15) #charged lepton
                  and genParts[index].genPartIdxMother >= 0 and (genParts[genParts[index].genPartIdxMother].pdgId == 23 #parent is z-boson
                                                                 or genParts[genParts[index].genPartIdxMother].pdgId == 25)): #parent is h-boson
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
                print "Z info replacement was successful!"
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

    def check_trig(self, trigObjs, lepton, isMuon):
        if isMuon :
            bit_1 = 1#3 #2 #Iso 1 muon
            bit_2 = 10 # bit_1 # 1024 #Mu50
        else :
            if self.runningEra == 1:
                bit_1 = 10 #1024 #32_L1DoubleEG_AND_L1SingleEGOr
                bit_2 = bit_1 #no second trigger
            else :
                bit_1 = 1 #2 # WPTight 1 ele
                bit_2 = bit_1 # no second trigger
        deltaR_match = 0.2
        deltaPt_match = 10 #fractional match, > ~5 --> no pT matching
        result = 0
        passedBit1 = False
        passedBit2 = False
        pdg = 13
        name = "a Muon"
        if not isMuon:
            pdg = 11
            name = "an Electron"
        if self.verbose > 9:
            print " Event", self.seen, ": Printing trigger object info for matching to a lepton with bits", (1<<bit_1), "and", (1<<bit_2)
            print " lepton pt, eta, phi =", lepton.pt, lepton.eta, lepton.phi
        for i_trig in range(len(trigObjs)):
            trigObj = trigObjs[i_trig]
            if abs(trigObj.id) != pdg:
                continue
            passBit1 = trigObj.filterBits & (1<<bit_1) != 0
            passBit2 = trigObj.filterBits & (1<<bit_2) != 0
            if self.verbose > 9:
                print "  Trigger object", i_trig, "for",name,"has filterBits", trigObj.filterBits, "pt, eta, phi =", trigObj.pt, trigObj.eta, trigObj.phi
            if passBit1 or passBit2:
                if self.verbose > 9:
                    print "   Trigger object", i_trig,"passed bit check, trig pt =", trigObj.pt, "lepton pt =", lepton.pt
                if abs(lepton.pt - trigObj.pt) < deltaPt_match*lepton.pt:
                    deltaEta = abs(lepton.eta - trigObj.eta)
                    deltaPhi = abs(lepton.phi - trigObj.phi)
                    if deltaPhi > math.pi:
                        deltaPhi = abs(2*math.pi - deltaPhi)
                    if self.verbose > 9:
                        print "    Trigger object passed pt check, trig eta, phi =", trigObj.eta, "," , trigObj.phi,\
                            "lepton eta, phi =", lepton.eta, ",", lepton.phi
                    deltaR = math.sqrt(deltaEta*deltaEta + deltaPhi*deltaPhi)
                    if deltaR < deltaR_match:
                        if self.verbose > 2:
                            print " Event",self.seen, "Trigger object",i_trig,"passed matching, pass bit1 =", passBit1, "pass bit2 =", passBit2
                        # if not isMuon:
                        result = 1
                        return result
                        # passedBit1 = passedBit1 or passBit1
                        # passedBit2 = passedBit2 or passBit2
        return 0 #passedBit1 + 2*passedBit2
                        
    # Main processing loop
    def analyze(self, event):
        ############################
        #     Begin event loop     #
        ############################
        #increment event count
        self.seen = self.seen + 1
        #record negative events for proper normalization
        if self.isData == 0 and event.genWeight < 0.:
            self.negativeEvents = self.negativeEvents + 1
        if(self.startEvent > self.seen): #continue until reach desired starting point
            return False
        if(self.startEvent > 1 and self.startEvent == self.seen):
            print "***Found starting event", self.startEvent
        if(self.maxEvents > 0 and self.seen-self.startEvent >= self.maxEvents) : #exit if processed maximum events
            print "Processed the maximum number of events,", self.maxEvents
            self.endJob()
            exit()        
        if self.verbose > 9:
            print "***Processing event", self.seen
            
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT       = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        taus      = Collection(event, "Tau")
        jets      = Collection(event, "Jet")
        PuppiMET  = Object(event, "PuppiMET")
        trigObjs  = Collection(event, "TrigObj")
        
        ############################
        #    Trigger parameters    #
        ############################
        doTriggerMatching = False #whether or not to require the matched trigger
        
        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT electron trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT muon trigger in 2017

        ## Non-trigger lepton parameters ##
        minmuptlow  = 10.
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
        muonLowTriggered = False
        muonHighTriggered = False
        electronTriggered = False        
        if self.runningEra == 0 :
            muonLowTriggered = HLT.IsoMu24
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele27_WPTight_Gsf
        elif self.runningEra == 1 :
            muonLowTriggered = HLT.IsoMu27
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
        elif self.runningEra == 2 :
            muonLowTriggered = HLT.IsoMu24
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele32_WPTight_Gsf
        muonTriggered = muonLowTriggered or muonHighTriggered
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event", self.seen, "muonTriggered =",muonTriggered,"electronTriggered =",electronTriggered
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
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print "Event", self.seen, ": printing electron info..."
            for index in range(len(electrons)) :
                if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                    print " Electron", index, "pt =", electrons[index].pt, "WPL =", electrons[index].mvaFall17V2Iso_WPL, \
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
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print "Event", self.seen, ": printing muon info..."
            for index in range(len(muons)) :
                if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                    print " Muon", index, "pt =", muons[index].pt, "IDL =", muons[index].looseId, "IDM =", muons[index].tightId, \
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
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print "Event", self.seen, ": printing tau info..."
            for index in range(len(taus)) :
                if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                    print " Tau", index, "pt =", taus[index].pt, "AntiMu =", taus[index].idDeepTau2017v2p1VSmu, "AntiEle =", \
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

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event",self.seen,"lepton counts: ntau (N before IDs) =",nTaus,"(", len(taus),") nelectron (N before IDs) =",nElectrons,"(", len(electrons),") nmuon (N before IDs) =",\
                nMuons,"(",len(muons),") met =",PuppiMET.pt

        if nElectrons + nMuons + nTaus < 2:
            return False

        ### Add lepton trigger requiring that lepton ###
        electronTriggered = electronTriggered and nElectrons > 0
        muonTriggered = muonTriggered and nMuons > 0
        if not muonTriggered and not electronTriggered:
            return False
        
        ####################################
        #  Check leptons against triggers  #
        ####################################
        if doTriggerMatching:
            if muonTriggered:
                muonTrig = False
                # muonLoTrig = False
                # muonHiTrig = False
                #check if a selected muon matches with the muon triggers of interest
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing muon trigger info..."
                for i_muon in range(nMuons):
                    hasFired = self.check_trig(trigObjs, muons[muon_dict[i_muon]], True)
                    if hasFired > 0: # 1 = low, 2 = high, 3 = both
                        muonTrig  = True
                        # muonLoTrig = muonLoTrig or hasFired == 1 or hasFired == 3
                        # muonHiTrig = muonHiTrig or hasFired > 1
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Muon",i_muon,"has hasFired =",hasFired
                if self.verbose > 0 and ((muonTriggered and not muonTrig) ): #or (muonLowTriggered and not muonLoTrig) or (muonHighTriggered and not muonHiTrig)) :
                    print "Event", self.seen, "has muon triggered values changed after mapping! There are", nMuons, "muons..."
                    print " Muon triggers before: trig =", muonTriggered, "low =", muonLowTriggered, "high =", muonHighTriggered
                    print " Muon triggers mapped: trig =", muonTrig #, "low =", muonLoTrig, "high =", muonHiTrig
                    print " Electron triggered =", electronTriggered
                muonTriggered     = muonTrig
                # muonLowTriggered  = muonLowTriggered  and muonLoTrig
                # muonHighTriggered = muonHighTriggered and muonHiTrig
            if electronTriggered:
                electronTriggered = False
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing electron trigger info..."
                for i_elec in range(nElectrons):
                    hasFired = self.check_trig(trigObjs, electrons[elec_dict[i_elec]], False)
                    if hasFired > 0:
                        electronTriggered = True
                        break
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Electron", i_elec, "has hasFired =", hasFired
                if self.verbose > 0 and not electronTriggered:
                    print "Event", self.seen, "has electron triggered value changed after mapping! There are", nElectrons, "electrons..."
        
        if not electronTriggered and not muonTriggered :
            self.failTrigMap = self.failTrigMap + 1
            return False
        
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

        if mumu :
            if not muonTriggered:
                return False
            if not muonLowTriggered : #only passed high pt trigger
                if not (lep1.pt > 50 or lep2.pt > 50.) :
                    return False                
        elif ee :
            if not electronTriggered :
                return False
        elif mutau :
            if not muonTriggered:
                return False
            if not muonLowTriggered : #only passed high pt trigger
                if not (lep1.pt > 50) :
                    return False                
        elif etau :
            if not electronTriggered :
                return False
        elif emu:
            #check triggers with threshold on triggering lepton
            if not ((muonTriggered and lep2.pt > minmupt) or (electronTriggered and lep1.pt > minelept)) :
                return False
            if not muonLowTriggered and not (electronTriggered and lep1.pt > minelept)  : #only passed high pt muon trigger
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

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "passing event", self.seen

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
        # Fill trigger info
        self.out.fillBranch("muonLowTrigger", muonLowTriggered)
        self.out.fillBranch("muonHighTrigger", muonHighTriggered)
        self.out.fillBranch("electronTrigger", electronTriggered)
            
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
leptonConstr = lambda runningEra, maxEvents, startEvent, isData, saveZ : exampleProducer(runningEra, maxEvents, startEvent, isData, saveZ)
