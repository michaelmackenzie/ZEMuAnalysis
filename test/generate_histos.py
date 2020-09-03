import ROOT
import math
import argparse
import numpy as np
import array
from Simplified_Workflow_Handler import Simplified_Workflow_Handler

############################################################################
#                                                                          #
#----------------------- Some bools to be initialized ---------------------#
#                                                                          #
############################################################################
p = argparse.ArgumentParser(description='Select whether to fill the histograms after pre-selection or selection')
p.add_argument('runningEra_option', help='Type <<0>> for 2016, <<1>> for 2017, <<2>> for 2018, <<3>> for combination 2016+2017')
p.add_argument('doFullSel_option', help='Do full selection or not')
p.add_argument('inputfile_option', help='Provide input file name')
p.add_argument('outputfile_option', help='Provide output file name')
p.add_argument('channel_option', help='Type <<0>> for e+mu, <<1>> for e+tau, or <<2>> for mu+tau')
args = p.parse_args()

runningEra = int(args.runningEra_option)
doFullSel = args.doFullSel_option == '1'
input_filename = args.inputfile_option
output_filename = args.outputfile_option
channel = int(args.channel_option)

#-------------------------#
myWF = Simplified_Workflow_Handler(runningEra)

verbose = 0


############################################################################
#                                                                          #
#-------------------------- Integrated luminosity -------------------------#
#                                                                          #
############################################################################
#Normalize to this luminsity, in fb-1
if runningEra == 0:
    luminosity_norm = 35.92
    jetIdflag = 7
    jetPUIdflag = 6
if runningEra == 1:
    luminosity_norm = 41.53
    jetIdflag = 4
    jetPUIdflag = 6
if runningEra == 2:
    luminosity_norm = 59.74
    jetIdflag = 4
    jetPUIdflag = 6

############################################################################
#                                                                          #
#-------------------- Get files and normalization map  --------------------#
#                                                                          #
############################################################################

# Get the files and the names of the samples
sample_name = input_filename.split("_")[2]

#Understand if this is data or MC
isData = False
if "SingleMu" in sample_name or "SingleEle" in sample_name :
    isData = True
    print "Analyzing a data sample..."

# Get the normalization
Norm_Map = myWF.get_normalizations_map(runningEra)


############################################################################
#                                                                          #
#---------------------- Define selection parameters -----------------------#
#                                                                          #
############################################################################
#Define relevant mass range
mll_min = 75.
mll_max = 160.
mll_bin = 2
if channel != 0 : #lower mass min in tau cases
    mll_min = 50.
    mll_bin = 5
mll_nbins = int(round((mll_max-mll_min)/mll_bin))
if mll_nbins%2 != 0: #force even number of bins to allow at least 1 rebinning
    mll_nbins = mll_nbins + 1

#whether to use selection criteria or not for lepton vetos
doCountingSelection = True
minmupt_count = 10.
muonIso_count = 4
muonId_count = 2 # 1 = loose, 2 = medium, 3 = tight
minelept_count = 15.
eleId_count = 2 #1 = WPL, 2 = WP80, 3 = WP90
mintaupt_count = 20.
tauAntiEle_count = 8
tauAntiMu_count = 2
tauIdDecay_count = True

if channel == 0:
    doCountingSelection = True

############################################################################
#                                                                          #
#------------------------------ Create histos -----------------------------#
#                                                                          #
############################################################################

##Get the handlers for all the histos and graphics
h_base  = dict()

list_histos = ["h_Mmumu", "h_Mee","h_Mmue", "h_lep1pt",
               "h_lep2pt", "h_lep1eta", "h_lep2eta", "h_lep1phi",
               "h_lep2phi", "h_njets25", "h_met_sumEt",
               "h_met_pt", "h_jetptmax", "h_npvs", "h_nbjets25",
               "h_btagid", "h_njets25dr", "h_jetlep1dr", "h_jetlep2dr",
               "h_leppt", "h_lepptoverm", "h_lep1weight", "h_lep2weight",
               "h_cuts", "h_puweight", "h_trigger",
               "h_nelec", "h_nmuon", "h_ntau"]

h_base[list_histos[0]]  = ROOT.TH1F(list_histos[0], "M_{#mu#mu}", mll_nbins, mll_min, mll_max)
h_base[list_histos[1]]  = ROOT.TH1F(list_histos[1], "M_{ee}", mll_nbins, mll_min, mll_max)
h_base[list_histos[2]]  = ROOT.TH1F(list_histos[2], "M_{#mu e}", mll_nbins, mll_min, mll_max)
h_base[list_histos[3]]  = ROOT.TH1F(list_histos[3], "p_{T} of the 1st lepton", 70, 10., 80.)
h_base[list_histos[4]]  = ROOT.TH1F(list_histos[4], "p_{T} of the 2nd lepton", 70, 10., 80.)
h_base[list_histos[5]]  = ROOT.TH1F(list_histos[5], "#eta of the 1st lepton", 30, -2.6, 2.6)
h_base[list_histos[6]]  = ROOT.TH1F(list_histos[6], "#eta of the 2nd lepton", 30, -2.6, 2.6)
h_base[list_histos[7]]  = ROOT.TH1F(list_histos[7], "#phi of the 1st lepton", 30, -3.15, 3.15)
h_base[list_histos[8]]  = ROOT.TH1F(list_histos[8], "#phi of the 2nd lepton", 30, -3.15, 3.15)
h_base[list_histos[9]]  = ROOT.TH1F(list_histos[9], "N_{jets} above 25 GeV", 10, 0, 10.)
h_base[list_histos[10]] = ROOT.TH1F(list_histos[10], "MET sumEt puppi", 100, 0., 1000.)
h_base[list_histos[11]] = ROOT.TH1F(list_histos[11], "MET pt puppi", 25, 0., 50.)
h_base[list_histos[12]] = ROOT.TH1F(list_histos[12], "p_{T} of the hardest jet", 50, 25., 100.)
h_base[list_histos[13]] = ROOT.TH1F(list_histos[13], "pile up",75,0,75)
h_base[list_histos[14]] = ROOT.TH1F(list_histos[14], "N_{bjets} above 25 GeV", 10, 0, 10.)
h_base[list_histos[15]] = ROOT.TH1F(list_histos[15], "bJet DeepB Value of Highest pT Jet", 55, -0.1, 1.)
h_base[list_histos[16]] = ROOT.TH1F(list_histos[16], "N_{jets} above 25 GeV and #DeltaR > 0.3 from leptons", 10, 0, 10.)
h_base[list_histos[17]] = ROOT.TH1F(list_histos[17], "hardest jet #DeltaR from lepton 1", 60, 0, 6.)
h_base[list_histos[18]] = ROOT.TH1F(list_histos[18], "hardest jet #DeltaR from lepton 2", 60, 0, 6.)
h_base[list_histos[19]] = ROOT.TH1F(list_histos[19], "pT_{ll}",  50, 0., 100.)
h_base[list_histos[20]] = ROOT.TH1F(list_histos[20], "pT_{ll}/M_{ll}",  50, 0., 5.)
h_base[list_histos[21]] = ROOT.TH1F(list_histos[21], "l_{1} weight",  50, 0., 2.)
h_base[list_histos[22]] = ROOT.TH1F(list_histos[22], "l_{2} weight",  50, 0., 2.)
h_base[list_histos[23]] = ROOT.TH1F(list_histos[23], "Cut flow", 10, 0, 10.)
h_base[list_histos[24]] = ROOT.TH1F(list_histos[24], "PU weight",  50, 0., 2.)
h_base[list_histos[25]] = ROOT.TH1F(list_histos[25], "Trigger status",  10, -0.5, 9.5)
h_base[list_histos[26]] = ROOT.TH1F(list_histos[26], "Number of electrons",  10, 0, 10)
h_base[list_histos[27]] = ROOT.TH1F(list_histos[27], "Number of muons"    ,  10, 0, 10)
h_base[list_histos[28]] = ROOT.TH1F(list_histos[28], "Number of taus"     ,  10, 0, 10)

##Open the output
fOut = ROOT.TFile(output_filename,"RECREATE")
fOut.cd()

############################################################################
#                                                                          #
#------------------------------ Create output root files  -----------------#
#                                                                          #
############################################################################

#Variables to go in the tree
_FourlepMass = np.zeros(1, dtype=float)
_met         = np.zeros(1, dtype=float)
_jetptmax    = np.zeros(1, dtype=float)
_mcweight    = np.zeros(1, dtype=float)
_lep1pt      = np.zeros(1, dtype=float)
_lep2pt      = np.zeros(1, dtype=float)

tree_signalreg = ROOT.TTree('signaltree','tree with branches')
tree_signalreg.Branch('M_ll',_FourlepMass,'M_ll/D')
tree_signalreg.Branch('met',_met,'met/D')
tree_signalreg.Branch('jetptmax',_jetptmax,'jetptmax/D')
tree_signalreg.Branch('mcweight',_mcweight,'mcweight/D')
tree_signalreg.Branch('lep1pt',_lep1pt,'lep1pt/D')
tree_signalreg.Branch('lep2pt',_lep2pt,'lep2pt/D')

print "Processing Sample ", sample_name, "with channel value", channel
##Loop on events
if not isData:
    if not sample_name in Norm_Map:
        print "WARNING! No norm factor in Norm_Map found! Setting to Norm_Map[HMuTau]"
        norm_factor = Norm_Map["HMuTau"]
    else :
        norm_factor = Norm_Map[sample_name]
    print "Norm_Map[", sample_name, "]: ", norm_factor
    norm_factor = norm_factor*luminosity_norm


root_file = ROOT.TFile(input_filename)
mytree = root_file.Get("Events")

Nevts_per_sample   = 0. # Count the number of events in input per each sample processed
Nevts_selected     = 0. # Count the number of events survived per each sample processed
Nevts_expected     = 0. # Number of expected events from weights

nentries = mytree.GetEntriesFast()

#Initializing variables
lep1_FourMom = ROOT.TLorentzVector()
lep2_FourMom = ROOT.TLorentzVector()

muon_ptmin = 25. #trigger
electron_ptmin = 33. #trigger
require_both_high_pt = True #apply trigger pT thresholds to both
muon_lowptmin = 10. #object
electron_lowptmin = 15. #object
tau_ptmin = 20. #object

if runningEra == 1 :
    muon_ptmin = 28. #higher threshold
if require_both_high_pt :
    muon_lowptmin = muon_ptmin
    electron_lowptmin = electron_ptmin

print "This sample has ", nentries, " events"

#create a char array
Muon_pfIsoId = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
Tau_idAntiEle = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
Tau_idAntiMu = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
mytree.SetBranchAddress("Muon_pfIsoId", Muon_pfIsoId)
mytree.SetBranchAddress("Tau_idAntiEle", Tau_idAntiEle)
mytree.SetBranchAddress("Tau_idAntiMu", Tau_idAntiMu)
for jentry in xrange(nentries):
    ientry = mytree.LoadTree( jentry )
    if ientry < 0:
        break
    nb = mytree.GetEntry(jentry )
    if nb <= 0:
        continue

    Nevts_per_sample = Nevts_per_sample + 1

    if (Nevts_per_sample/100000.).is_integer() :
        print "Processed ", Nevts_per_sample, " events..."

    #count the number of leptons in the event
    nElectrons = 0
    nMuons = 0
    nTaus = 0
    elec_dict = dict() # save a dictionary to find the objects again
    muon_dict = dict()
    tau_dict = dict()

    if verbose > 0 and jentry%10 == 0:
        print "*******************************************************"
        print "Entry",jentry

    if doCountingSelection :
        for index in range(mytree.nElectron) :
            doCount = mytree.Electron_pt[index] > minelept_count
            if eleId_count == 1 :
                doCount = doCount and mytree.Electron_mvaFall17V2Iso_WPL [index]
            elif eleId_count == 2 :
                doCount = doCount and mytree.Electron_mvaFall17V2Iso_WP80[index]
            elif eleId_count == 3 :
                doCount = doCount and mytree.Electron_mvaFall17V2Iso_WP90[index]
            if doCount :
                elec_dict[nElectrons] = index
                nElectrons = nElectrons + 1
            if verbose > 0 and jentry%10 == 0:
                print ("Electron " + str(index)
                       + " pT " + str(mytree.Electron_pt[index])
                       + " WPL "  + str(mytree.Electron_mvaFall17V2Iso_WPL [index]) 
                       + " WP80 " + str(mytree.Electron_mvaFall17V2Iso_WP80[index]) 
                       + " WP90 " + str(mytree.Electron_mvaFall17V2Iso_WP90[index])
                       + " doCount " + str(doCount))
        for index in range(mytree.nMuon) :
            doCount = mytree.Muon_pt[index] > minmupt_count
            if muonId_count == 1 :
                doCount = doCount and mytree.Muon_looseId [index]
            elif muonId_count == 2 :
                doCount = doCount and mytree.Muon_mediumId [index]
            elif muonId_count == 3 :
                doCount = doCount and mytree.Muon_tightId [index]
            doCount = doCount and Muon_pfIsoId[index] >= muonIso_count
            if doCount :
                muon_dict[nMuons] = index
                nMuons = nMuons + 1
            if verbose > 0 and jentry%10 == 0:
                print ("Muon " + str(index)
                       + " pT " + str(mytree.Muon_pt[index])
                       + " id loose "  + str(mytree.Muon_looseId[index]) 
                       + " id medium " + str(mytree.Muon_mediumId[index]) 
                       + " id tight " + str(mytree.Muon_tightId[index])
                       + " iso id " + str(Muon_pfIsoId[index])
                       + " doCount " + str(doCount))
        for index in range(mytree.nTau) :
            doCount = mytree.Tau_pt[index] > mintaupt_count
            doCount = doCount and Tau_idAntiEle[index] >= tauAntiEle_count
            doCount = doCount and Tau_idAntiMu[index] >= tauAntiMu_count
            doCount = doCount and (mytree.Tau_idDecayMode[index] or not tauIdDecay_count)
            if doCount :
                tau_dict[nTaus] = index
                nTaus = nTaus + 1
            if verbose > 0 and jentry%10 == 0:
                print ("Tau " + str(index)
                       + " pT " + str(mytree.Tau_pt[index])
                       + " antiEle id " + str(Tau_idAntiEle[index])
                       + " antiMu id " + str(Tau_idAntiMu[index])
                       + " decay id " + str(mytree.Tau_idDecayMode[index])
                       + " doCount " + str(doCount))
    else :
        nElectrons = mytree.nElectron
        nMuons     = mytree.nMuon
        nTaus      = mytree.nTau
        for index in range(nElectrons):
            elec_dict[index] = index
        for index in range(nMuons):
            muon_dict[index] = index
        for index in range(nTaus):
            tau_dict[index] = index

    if channel == 0 and nMuons + nElectrons != 2:
        continue
    elif channel == 1 and not (nMuons == 0 and nTaus == 1 and nElectrons == 1):
        continue
    elif channel == 2 and not (nMuons == 1 and nTaus == 1 and nElectrons == 0):
        if verbose > 1 or (jentry%10 == 0 and verbose > 0):
            print "Event failed with", nMuons, "(",mytree.nMuon, ") muons, ", nElectrons,"(",mytree.nElectron, ") electrons and", nTaus,"(",mytree.nTau, ") taus"
        continue
    if verbose > 1 or (jentry%10 == 0 and verbose > 0):
        print "Event passed with", nMuons, "(",mytree.nMuon, ") muons, ", nElectrons,"(",mytree.nElectron, ") electrons and", nTaus,"(",mytree.nTau, ") taus"

    if nMuons == 2 :

        lep1_pt = mytree.Muon_pt    [muon_dict[0]]
        lep1_eta = mytree.Muon_eta  [muon_dict[0]]
        lep1_phi = mytree.Muon_phi  [muon_dict[0]]
        lep1_mass = mytree.Muon_mass[muon_dict[0]]

        lep2_pt = mytree.Muon_pt    [muon_dict[1]]
        lep2_eta = mytree.Muon_eta  [muon_dict[1]]
        lep2_phi = mytree.Muon_phi  [muon_dict[1]]
        lep2_mass = mytree.Muon_mass[muon_dict[1]]
        if doFullSel and (lep1_pt <= muon_ptmin and lep2_pt <= muon_ptmin) :
            continue
        if lep1_pt <= muon_lowptmin or lep2_pt <= muon_lowptmin :
            continue
    elif nElectrons == 2 :

        lep1_pt = mytree.Electron_pt    [elec_dict[0]]
        lep1_eta = mytree.Electron_eta  [elec_dict[0]]
        lep1_phi = mytree.Electron_phi  [elec_dict[0]]
        lep1_mass = mytree.Electron_mass[elec_dict[0]]

        lep2_pt = mytree.Electron_pt    [elec_dict[1]]
        lep2_eta = mytree.Electron_eta  [elec_dict[1]]
        lep2_phi = mytree.Electron_phi  [elec_dict[1]]
        lep2_mass = mytree.Electron_mass[elec_dict[1]]
        if doFullSel and (lep1_pt <= electron_ptmin and lep2_pt <= electron_ptmin) :
            continue
        if lep1_pt <= electron_lowptmin or lep2_pt <= electron_lowptmin :
            continue
        if not mytree.Electron_mvaFall17V2Iso_WP80[elec_dict[0]] or not mytree.Electron_mvaFall17V2Iso_WP80[elec_dict[1]] :
            continue

    elif channel == 0 : #e+mu
        lep1_pt = mytree.Muon_pt    [muon_dict[0]]
        lep1_eta = mytree.Muon_eta  [muon_dict[0]]
        lep1_phi = mytree.Muon_phi  [muon_dict[0]]
        lep1_mass = mytree.Muon_mass[muon_dict[0]]

        lep2_pt = mytree.Electron_pt    [elec_dict[0]]
        lep2_eta = mytree.Electron_eta  [elec_dict[0]]
        lep2_phi = mytree.Electron_phi  [elec_dict[0]]
        lep2_mass = mytree.Electron_mass[elec_dict[0]]
        if doFullSel and (lep1_pt <= muon_ptmin and lep2_pt <= electron_ptmin) :
            continue
        if lep1_pt <= muon_lowptmin or lep2_pt <= electron_lowptmin :
            continue
        if not mytree.Electron_mvaFall17V2Iso_WP80[elec_dict[0]] :
            continue

    elif channel == 1 : #e+tau
        lep1_pt   = mytree.Electron_pt  [elec_dict[0]]
        lep1_eta  = mytree.Electron_eta [elec_dict[0]]
        lep1_phi  = mytree.Electron_phi [elec_dict[0]]
        lep1_mass = mytree.Electron_mass[elec_dict[0]]

        lep2_pt   = mytree.Tau_pt  [tau_dict[0]]
        lep2_eta  = mytree.Tau_eta [tau_dict[0]]
        lep2_phi  = mytree.Tau_phi [tau_dict[0]]
        lep2_mass = mytree.Tau_mass[tau_dict[0]]

        if lep1_pt <= electron_ptmin :#or lep2_pt <= tau_ptmin :
            continue
        if not mytree.Electron_mvaFall17V2Iso_WP80[0] :
            continue

    elif channel == 2 : #mu+tau
        lep1_pt   = mytree.Muon_pt  [muon_dict[0]]
        lep1_eta  = mytree.Muon_eta [muon_dict[0]]
        lep1_phi  = mytree.Muon_phi [muon_dict[0]]
        lep1_mass = mytree.Muon_mass[muon_dict[0]]

        lep2_pt   = mytree.Tau_pt  [tau_dict[0]]
        lep2_eta  = mytree.Tau_eta [tau_dict[0]]
        lep2_phi  = mytree.Tau_phi [tau_dict[0]]
        lep2_mass = mytree.Tau_mass[tau_dict[0]]

        if lep1_pt <= muon_ptmin or lep2_pt <= tau_ptmin :
            continue
    else : #no selection
        continue    
    lep1_FourMom.SetPtEtaPhiM(lep1_pt,lep1_eta,lep1_phi,lep1_mass)
    lep2_FourMom.SetPtEtaPhiM(lep2_pt,lep2_eta,lep2_phi,lep2_mass)
    Zcand_FourMom = lep1_FourMom + lep2_FourMom

    jet_FourMom  = ROOT.TLorentzVector()
    njets_25     =  0
    njets_25_dr  =  0   #njets with delta r > 0.3 from leptons
    nbjets_25    =  0
    nbjets_25_dr =  0   #nbjets with delta r > 0.3 from leptons
    bjetusedr    = True #use delta r cut when doing b-jet selection cut
    jetptmax     =  0.  #hardest jet pT
    jetptusedr   = True #use the delta r cut when getting hardest jet
    jetbtag      = -2.  #btag score for hardest jet
    jetlep1dr    = -1.  #delta r between hardest jet and lep 1
    jetlep2dr    = -1.  #delta r between hardest jet and lep 2
    
    for jetcount in xrange(mytree.nJet) :

        if mytree.Jet_jetId[jetcount] < jetIdflag :
            continue

        jet_pt = mytree.Jet_pt[jetcount]
        jet_eta = mytree.Jet_eta[jetcount]
        jet_phi = mytree.Jet_phi[jetcount]
        jet_mass = mytree.Jet_mass[jetcount]

        if jet_pt < 50. and mytree.Jet_puId[jetcount] < jetPUIdflag :
            continue

        jet_FourMom.SetPtEtaPhiM(jet_pt,jet_eta,jet_phi,jet_mass)


        deltaR_lep1_jet = jet_FourMom.DeltaR(lep1_FourMom)
        deltaR_lep2_jet = jet_FourMom.DeltaR(lep2_FourMom)

        if deltaR_lep1_jet < 0.3 or deltaR_lep2_jet < 0.3 :
            continue


        if pt_of_jet > 25. :
            njets_25 = njets_25 + 1    
            if jet_pt > jetptmax :
                jetptmax = jet_pt
                if hasattr(mytree, 'Jet_btagDeepB') :
                    jetbtag = mytree.Jet_btagDeepB[jetcount]
            if hasattr(mytree, 'Jet_btagDeepB') and mytree.Jet_btagDeepB[jetcount] > 0.4184 :
                nbjets_25 = nbjets_25 + 1
        #End jet loop
    met_pt_puppi = mytree.PuppiMET_pt
    met_sumEt_puppi = mytree.PuppiMET_sumEt

    jetsel = jetptmax < 78.
    metsel = met_pt_puppi < 28.
    select_bool = (jetsel and metsel and nbjets_25 == 0) or not doFullSel

    if select_bool :
        Nevts_selected = Nevts_selected + 1

    nPV = mytree.PV_npvs

    ############################################################################
    #                                                                          #
    #--------------------- Determine the total event weight -------------------#
    #                                                                          #
    ############################################################################

    #Lepton scale factors
    lep1_weight = 1.
    lep2_weight = 1.
    isSingleMuTrigger_LOW = mytree.HLT_IsoMu24
    if runningEra == 1:
        isSingleMuTrigger_LOW = mytree.HLT_IsoMu27
    isSingleMuTrigger_HIGH = mytree.HLT_Mu50
    if runningEra == 0 :
        isSingleEleTrigger = mytree.HLT_Ele27_WPTight_Gsf
    elif runningEra == 1 :
        isSingleEleTrigger = mytree.HLT_Ele32_WPTight_Gsf_L1DoubleEG
    elif runningEra == 2 :
        isSingleEleTrigger = mytree.HLT_Ele32_WPTight_Gsf
    if not isData :
        if nMuons == 2 : # Get muon scale factors, which are different for two groups of datasets, and weight them for the respective integrated lumi 

        if mytree.nMuon == 2 : # Get muon scale factors, which are different for two groups of datasets, and weight them for the respective integrated lumi 

            lep1_weight = myWF.get_muon_scale(lep1_pt,lep1_eta,isSingleMuTrigger_LOW,runningEra,isMuTrigger)
            lep2_weight = myWF.get_muon_scale(lep2_pt,lep2_eta,isSingleMuTrigger_LOW,runningEra,isMuTrigger)

        ############### ELECTRON SFs ##############
        elif nElectrons == 2 :
            lep1_weight = myWF.get_ele_scale(lep1_pt, lep1_eta + mytree.Electron_deltaEtaSC[elec_dict[0]],runningEra)
            lep2_weight = myWF.get_ele_scale(lep2_pt, lep2_eta + mytree.Electron_deltaEtaSC[elec_dict[1]],runningEra)
        elif nMuons == 1 :
            lep1_weight = myWF.get_muon_scale(lep1_pt,lep1_eta,isSingleMuTrigger_LOW,runningEra)
            if nElectrons == 1 :
                lep2_weight = myWF.get_ele_scale(lep2_pt, lep2_eta + mytree.Electron_deltaEtaSC[elec_dict[0]],runningEra)
        ############### Multiply weights and SFs for MC. Set weight to 1 for data ###############
        MC_Weight = mytree.genWeight
        PU_Weight = 1.
        if hasattr(mytree, 'puWeight') :
            PU_Weight = mytree.puWeight # Add Pile Up weight

        Event_Weight = norm_factor*MC_Weight*PU_Weight/math.fabs(MC_Weight) # Just take the sign of the gen weight
        Event_Weight = Event_Weight*lep1_weight*lep2_weight

    else:
        Event_Weight = 1. #is data --> no weight

    #Fill the tree variables
    _FourlepMass[0] = Zcand_FourMom.M()
    _met[0]         = met_pt_puppi
    _jetptmax[0]    = jetptmax
    _mcweight[0]    = Event_Weight
    _lep1pt[0]      = lep1_pt
    _lep2pt[0]      = lep2_pt

    if nMuons != 2 and nElectrons != 2 and select_bool:
        Nevts_expected += Event_Weight # Increment the number of events survived in the analyzed sample
   
    ############################################################################
    #                                                                          #
    #------------------------------- Fill histos ------------------------------#
    #                                                                          #
    ############################################################################
    triggerStatus = isSingleMuTrigger_LOW + 2*isSingleMuTrigger_HIGH + 4*isSingleEleTrigger
    
    if nMuons != 2 and nElectrons != 2 :
        if select_bool :
            mll  = Zcand_FourMom.M()
            ptll = Zcand_FourMom.Pt()
            is_blind = ((mll > 84. and mll < 101.)
                        or (mll > 115. and mll < 135.)) and channel == 0
            
            if not isData or not is_blind :
                h_base["h_Mmue"].Fill(mll,Event_Weight)

            h_base["h_leppt"].Fill(ptll, Event_Weight)
            h_base["h_lepptoverm"].Fill(ptll/mll, Event_Weight)
            h_base["h_lep1pt"].Fill (lep1_pt, Event_Weight)
            h_base["h_lep2pt"].Fill (lep2_pt, Event_Weight)
            h_base["h_lep1eta"].Fill(lep1_eta,Event_Weight)
            h_base["h_lep2eta"].Fill(lep2_eta,Event_Weight)
            h_base["h_lep1phi"].Fill(lep1_phi,Event_Weight)
            h_base["h_lep2phi"].Fill(lep2_phi,Event_Weight)

            h_base["h_njets25"].Fill(njets_25,Event_Weight)
            h_base["h_njets25dr"].Fill(njets_25_dr,Event_Weight)
            h_base["h_nbjets25"].Fill(nbjets_25,Event_Weight)
            h_base["h_btagid"].Fill(jetbtag,Event_Weight)
            h_base["h_met_sumEt"].Fill(met_sumEt_puppi,Event_Weight)
            h_base["h_jetlep1dr"].Fill(jetlep1dr,Event_Weight)
            h_base["h_jetlep2dr"].Fill(jetlep2dr,Event_Weight)
            if not isData :
                if lep1_weight > 0. :
                    h_base["h_lep1weight"].Fill(lep1_weight,Event_Weight/lep1_weight)
                else :
                    h_base["h_lep1weight"].Fill(lep1_weight)        
                if lep2_weight > 0. :
                    h_base["h_lep2weight"].Fill(lep2_weight,Event_Weight/lep2_weight)
                else :
                    h_base["h_lep2weight"].Fill(lep2_weight)        
                if PU_Weight > 0. :
                    h_base["h_puweight"].Fill(PU_Weight, Event_Weight/PU_Weight)
                else :
                    h_base["h_puweight"].Fill(PU_Weight)
            h_base["h_npvs"].Fill(nPV,Event_Weight)
            h_base["h_cuts"].Fill(9,Event_Weight) #accepted events in cut flow
            h_base["h_trigger"].Fill(triggerStatus, Event_Weight)
            h_base["h_nelec"].Fill(mytree.nElectron, Event_Weight)
            h_base["h_nmuon"].Fill(mytree.nMuon, Event_Weight)
            h_base["h_ntau" ].Fill(mytree.nTau, Event_Weight)
            tree_signalreg.Fill()
            
        #End selection requirement
        
        if select_bool or (metsel and nbjets_25 == 0 and not jetsel) :
            h_base["h_jetptmax"].Fill(jetptmax,Event_Weight)
        if select_bool or (jetsel and nbjets_25 == 0 and not metsel) :
            h_base["h_met_pt"].Fill(met_pt_puppi,Event_Weight)
        #record the cut-flow of the selection
        h_base["h_cuts"].Fill(0,Event_Weight) # all events
        if jetsel :
            h_base["h_cuts"].Fill(1,Event_Weight)
        if metsel :
            h_base["h_cuts"].Fill(2,Event_Weight)
        if nbjets_25 == 0 :
            h_base["h_cuts"].Fill(3,Event_Weight)
            if jetsel : #nbjets + jetpt
                h_base["h_cuts"].Fill(4,Event_Weight)
            if metsel : #nbjets + metpt
                h_base["h_cuts"].Fill(5,Event_Weight)
                if jetsel : #nbjets + jetpt + metpt
                    h_base["h_cuts"].Fill(6,Event_Weight)
    #End histogram filling (nmuon == 1)
#End event loop
fOut.cd()
for hist_name in list_histos:
    h_base[hist_name].Write()
tree_signalreg.Write()
fOut.Close()

print "Number of expected events for ", luminosity_norm, " in fb-1, for sample " , sample_name
print "Number of events processed = ", Nevts_per_sample
print "Number of events selected = ", Nevts_selected
print "Number of events expected = ", Nevts_expected
print "###################"
print "###################"
