import ROOT
import math

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra, maxEvents, startEvent, isData):
        self.runningEra = runningEra
        self.maxEvents = maxEvents #for quick local testing
        self.startEvent = startEvent
        self.isData = isData
        self.seen = 0
        self.qcdSS = 0
        self.qcdOS = 0
        self.nominal = 0
        # if self.maxEvents == 1:
        #     self.verbose = 20
        # elif self.maxEvents > 0 and self.maxEvents < 10:
        #     self.verbose = 10
        # elif self.maxEvents > 0:
        #     self.verbose = 2
        # else:
        #     self.verbose = 1
        self.verbose = -1
        pass
    def beginJob(self):
        pass
    def endJob(self):
        print "From", self.seen, "events, nominal =", self.nominal, "QCD SS =", self.qcdSS, "QCD OS =", self.qcdOS
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
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

    # electron ID check
    def elec_id(self, electron, WP):
        if WP == 0: 
            return True
        elif WP == 1:
            return electron.mvaFall17V2Iso_WPL
        elif WP == 2:
            return electron.mvaFall17V2Iso_WP80
        elif WP == 3:
            return electron.mvaFall17V2Iso_WP90
        return False

    # tau ID check
    def tau_id(self, tau, useDeep, antiEle, antiMu, antiJet) :
        passed = True
        if useDeep:
            passed = passed and tau.idDeepTau2017v2p1VSe >= antiEle
            passed = passed and tau.idDeepTau2017v2p1VSmu >= antiMu
            passed = passed and tau.idDeepTau2017v2p1VSjet >= antiJet
            passed = passed and tau.idDecayModeNewDMs
        else:
            passed = passed and tau.idAntiEle >= antiEle
            passed = passed and tau.idAntiMu >= antiMu
            passed = passed and tau.idMVAnewDM2017v2 >= antiJet
            passed = passed and tau.idDecayMode
        return passed

    # Main processing loop
    def analyze(self, event):
        ############################
        #     Begin event loop     #
        ############################
        #increment event count
        self.seen = self.seen + 1
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
        trigObjs  = Collection(event, "TrigObj")
        
        ############################
        #    Trigger parameters    #
        ############################
        doTriggerMatching = True #whether or not to require the matched trigger
        
        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT electron trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT muon trigger in 2017

        ## Non-trigger lepton parameters ##
        minmuptlow  = 10.
        mineleptlow = 10.
        mintaupt    = 20.

        
        ############################
        #       Object IDs         #
        ############################

        ## muon isolation cut levels ##
        muonIsoVLoose  = 0.4
        muonIsoLoose   = 0.25 #eff ~ 0.98
        muonIsoMedium  = 0.20
        muonIsoTight   = 0.15 #eff ~ 0.95
        muonIsoVTight  = 0.10
        muonIsoVVTight = 0.05

        ## selection parameters ##
        minLepM     = 50. # generator only went down to 50 GeV/c^2
        maxLepM     = 170.

        # switch between tau IDs (deep NN IDs or old MVA IDs)
        useDeepNNTauIDs = True
        
        muonIso_DF  = muonIsoTight
        eleId_DF    = 2
        tauAntiEle = 1 # (bitmask) MVA: 8 = tight, 16 = very tight deepNN:  1 = VVVLoose 2 = VVLoose 4 = VLoose   8 = Loose
        #                                                                  16 = Medium  32 = Tight  64 = VTight 128 = VVTight
        tauAntiEle_etau = 50 #higher veto requirement for ee -> e fake tau
        tauAntiMu  = 10 # (bitmask) MVA: 1 = loose 2 = tight deepNN: 1 = VLoose 2 = Loose 4 = Medium 8 = Tight
        tauAntiJet = 50 # (bitmask) deepNN: 1 = VVVLoose 2 = VVLoose 4 = VLoose 8 = Loose 16 = Medium 32 = Tight 64 = VTight 128 = VVTight
        tauDeltaR  = 0.3

        ############################
        #     Veto object IDs      #
        ############################
        
        ## counting veto parameters ##
        doCountingSelection = True # else just use length of the array
        # muons
        minmupt_count = 10. # 3 GeV/c threshold in nanoAOD
        muonIso_count = muonIsoVLoose
        muonId_count = 1 # 1 = loose, 2 = medium, 3 = tight
        max_muon_eta = 2.4
        # electrons
        minelept_count = 10. # 5 GeV/c threshold in nanoAOD
        eleId_count = 1 #0 = none 1 = WPL, 2 = WP80, 3 = WP90        
        max_ele_eta = 2.5
        # taus
        mintaupt_count = 20.
        tauAntiEle_count = 1
        tauAntiMu_count = 10
        tauAntiJet_count = 50
        tauIso_count = 0
        tauIdDecay_count = True
        tauDeltaR_count = 0.3 #distance from selected electrons/muons
        max_tau_eta = 2.3

        ############################
        #     Begin selections     #
        ############################

        
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
            if (self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print "Event", self.seen, ": printing electron info..."
            for index in range(len(electrons)) :
                if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                    print " Electron", index, "pt =", electrons[index].pt, "WPL =", electrons[index].mvaFall17V2Iso_WPL, \
                        "WP80 =", electrons[index].mvaFall17V2Iso_WP80 
                ele_sc_eta = abs(electrons[index].eta + electrons[index].deltaEtaSC)
                if (electrons[index].pt > minelept_count and  ele_sc_eta < max_ele_eta
                    and (ele_sc_eta < 1.442 or ele_sc_eta > 1.566)
                    and self.elec_id(electrons[index], eleId_count)) :
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
                    abs(muons[index].eta) < max_muon_eta and
                    ((muonId_count == 1 and muons[index].looseId) or
                     (muonId_count == 2 and muons[index].mediumId) or
                     (muonId_count == 3 and muons[index].tightId)) and
                    muons[index].pfRelIso04_all < muonIso_count) :
                    #FIXME: Add dxy, dz cuts
                    muon_dict[nMuons] = index
                    nMuons = nMuons + 1
            ############################
            #       Count taus         #
            ############################
            if ((self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10):
                print "Event", self.seen, ": printing tau info..."
            for index in range(len(taus)) :
                if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                    print " Tau", index, "pt =", taus[index].pt, "AntiMu =", taus[index].idDeepTau2017v2p1VSmu, "AntiEle =", \
                        taus[index].idDeepTau2017v2p1VSe, "AntiJet =", taus[index].idDeepTau2017v2p1VSjet
                if (taus[index].pt > mintaupt_count and abs(taus[index].eta) < max_tau_eta
                    and self.tau_id(taus[index], useDeepNNTauIDs, tauAntiEle_count, tauAntiMu_count, tauAntiJet_count)) :
                    deltaRCheck = True
                    if tauDeltaR_count > 0 : #check for overlap with accepted lepton
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
                nMuons,"(",len(muons),")"

        if nElectrons + nMuons + nTaus < 2:
            return False

        ### Add lepton trigger requiring that lepton ###
        muonTriggered = muonTriggered and nMuons > 0
        if not muonTriggered:
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
        
        if nMuons != 1 or nTaus != 1:
            return False

        ############################
        #      QCD like ID         #
        ############################
        tau = taus[tau_dict[0]]
        muon = muons[muon_dict[0]]
        passed = True
        passed = passed and muon.tightId
        passed = passed and muon.pfRelIso04_all < muonIso_DF
        passed = passed and muon.pt > minmupt
        passed = passed and tau.pt > mintaupt
        passed = passed and muonTriggered
        if not passed:
            return False
        if muon.charge * tau.charge < 0:
            self.nominal = self.nominal + 1
        passed = passed and tau.idAntiMu == 0
        if not passed:
            return False
        if muon.charge * tau.charge < 0:
            self.qcdOS = self.qcdOS + 1
        else:
            self.qcdSS = self.qcdSS + 1

        ############################
        #     Mass filtering       #
        ############################
        
        lep_mass = (muon.p4() + tau.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
            return False


        
        ############################
        #      Accept event        #
        ############################
        if self.verbose == -1 :
            print event.event, event.run, event.luminosityBlock
            return True
        
        print "Passing event", self.seen, " --> printing event information!"
        print " nMuons =", nMuons, "nElectrons =", nElectrons, "nTaus =", nTaus, "low-trigger =", muonLowTriggered, "high-trigger =", muonHighTriggered
        if muon.charge*tau.charge < 0:
            print " Opposite sign event"
        else :
            print " Same sign event"
            
        ############################
        #     Print electrons      #
        ############################
        for index in range(len(electrons)) :
            print " Electron {} pt = {:.3f} WPL = {} WP80 = {} eta = {:.3f} SC_eta = {:.3f}".format(index,  electrons[index].pt, \
                                                                                                    electrons[index].mvaFall17V2Iso_WPL,\
                                                                                                    electrons[index].mvaFall17V2Iso_WP80,\
                                                                                                    electrons[index].eta,\
                                                                                                    abs(electrons[index].eta + electrons[index].deltaEtaSC))
        ############################
        #       Print muons        #
        ############################
        for index in range(len(muons)) :
            if index == muon_dict[0]:
                print " *Selection muon -->"
            print " Muon {} pt = {:.3f} IDL = {} IDM = {} IDT = {} iso = {:.5f} eta = {:.3f} dxy = {:.5f} dz = {:.5f}".format(index, muons[index].pt,\
                                                                                                                              muons[index].looseId,\
                                                                                                                              muons[index].mediumId, \
                                                                                                                              muons[index].tightId,\
                                                                                                                              muons[index].pfRelIso04_all,\
                                                                                                                              muons[index].eta,\
                                                                                                                              muons[index].dxy,\
                                                                                                                              muons[index].dz)
        ############################
        #       Print taus         #
        ############################
        for index in range(len(taus)) :
            if index == tau_dict[0]:
                print " *Selection tau -->"
            tau_s = " Tau {} pt = {:.3f} deep-AntiMu = {} (raw = {:.4f}) deep-AntiEle = {} deep-AntiJet = {}".format(index, taus[index].pt,\
                                                                                                                     taus[index].idDeepTau2017v2p1VSmu,\
                                                                                                                     taus[index].rawDeepTau2017v2p1VSmu,\
                                                                                                                     taus[index].idDeepTau2017v2p1VSe,\
                                                                                                                     taus[index].idDeepTau2017v2p1VSjet)
            tau_s = "{} MVA-AntiMu = {} MVA-AntiEle = {} MVA-AntiJet = {} DM = {} dxy = {:.5f} dz = {:.5f}".format(tau_s, taus[index].idAntiMu,\
                                                                                                                   taus[index].idAntiEle,\
                                                                                                                   taus[index].idMVAnewDM2017v2,\
                                                                                                                   taus[index].decayMode, \
                                                                                                                   taus[index].dxy, taus[index].dz)
            print tau_s

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra, maxEvents, startEvent, isData : exampleProducer(runningEra, maxEvents, startEvent, isData)
