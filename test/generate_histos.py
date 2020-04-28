import ROOT
import math
import argparse
import numpy as np
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
args = p.parse_args()

runningEra = int(args.runningEra_option)
doFullSel = args.doFullSel_option == '1'
input_filename = args.inputfile_option
output_filename = args.outputfile_option

#-------------------------#
myWF = Simplified_Workflow_Handler(runningEra)

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
    luminosity_norm = 41.48
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
               "h_cuts"]

h_base[list_histos[0]]  = ROOT.TH1F(list_histos[0], "M_{#mu#mu}", 50, 75., 110.)
h_base[list_histos[1]]  = ROOT.TH1F(list_histos[1], "M_{ee}", 50, 75., 110.)
h_base[list_histos[2]]  = ROOT.TH1F(list_histos[2], "M_{#mu e}", 50, 75., 110.)
h_base[list_histos[3]]  = ROOT.TH1F(list_histos[3], "p_{T} of the 1st lepton", 40, 27., 80.)
h_base[list_histos[4]]  = ROOT.TH1F(list_histos[4], "p_{T} of the 2nd lepton", 40, 32., 80.)
h_base[list_histos[5]]  = ROOT.TH1F(list_histos[5], "#eta of the 1st lepton", 30, -2.6, 2.6)
h_base[list_histos[6]]  = ROOT.TH1F(list_histos[6], "#eta of the 2nd lepton", 30, -2.6, 2.6)
h_base[list_histos[7]]  = ROOT.TH1F(list_histos[7], "#phi of the 1st lepton", 30, -3.15, 3.15)
h_base[list_histos[8]]  = ROOT.TH1F(list_histos[8], "#phi of the 2nd lepton", 30, -3.15, 3.15)
h_base[list_histos[9]]  = ROOT.TH1F(list_histos[9], "N_{jets} above 25 GeV", 10, 0, 10.)
h_base[list_histos[10]] = ROOT.TH1F(list_histos[10], "MET sumEt puppi", 100, 0., 1000.)
h_base[list_histos[11]] = ROOT.TH1F(list_histos[11], "MET pt puppi", 30, 0., 50.)
h_base[list_histos[12]] = ROOT.TH1F(list_histos[12], "p_{T} of the hardest jet", 40, 30., 100.)
h_base[list_histos[13]] = ROOT.TH1F(list_histos[13], "pile up",75,0,75)
h_base[list_histos[14]] = ROOT.TH1F(list_histos[14], "N_{bjets} above 25 GeV", 10, 0, 10.)
h_base[list_histos[15]] = ROOT.TH1F(list_histos[15], "bJet DeepB Value of Highest pT Jet", 100, -1., 1.)
h_base[list_histos[16]] = ROOT.TH1F(list_histos[16], "N_{jets} above 25 GeV and #DeltaR > 0.3 from leptons", 10, 0, 10.)
h_base[list_histos[17]] = ROOT.TH1F(list_histos[17], "hardest jet #DeltaR from lepton 1", 60, 0, 6.)
h_base[list_histos[18]] = ROOT.TH1F(list_histos[18], "hardest jet #DeltaR from lepton 2", 60, 0, 6.)
h_base[list_histos[19]] = ROOT.TH1F(list_histos[19], "Cut flow", 10, 0, 10.)

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

print "Processing Sample ", sample_name
##Loop on events
if not isData:
    norm_factor = Norm_Map[sample_name]*luminosity_norm
    print "Norm_Map[", sample_name, "]: ", Norm_Map[sample_name]
    
root_file = ROOT.TFile(input_filename)
mytree = root_file.Get("Events")

Nevts_per_sample   = 0. # Count the number of events in input per each sample processed
Nevts_selected     = 0. # Count the number of events survived per each sample processed
Nevts_expected     = 0. # Number of expected events from weights

nentries = mytree.GetEntriesFast()

#Initializing variables
lep1_FourMom = ROOT.TLorentzVector()
lep2_FourMom = ROOT.TLorentzVector()

muon_ptmin = 25.
electron_ptmin = 33.

# whether or not to reject jets overlapping with the e/mu
jet_delta_r_cut = True

print "This sample has ", mytree.GetEntriesFast(), " events"

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

    if mytree.nMuon == 2 :

        lep1_pt = mytree.Muon_pt[0]
        lep1_eta = mytree.Muon_eta[0]
        lep1_phi = mytree.Muon_phi[0]
        lep1_mass = mytree.Muon_mass[0]

        lep2_pt = mytree.Muon_pt[1]
        lep2_eta = mytree.Muon_eta[1]
        lep2_phi = mytree.Muon_phi[1]
        lep2_mass = mytree.Muon_mass[1]
        if doFullSel and (lep1_pt < muon_ptmin or lep2_pt < muon_ptmin) :
            continue
    elif mytree.nElectron == 2 :

        lep1_pt = mytree.Electron_pt[0]
        lep1_eta = mytree.Electron_eta[0]
        lep1_phi = mytree.Electron_phi[0]
        lep1_mass = mytree.Electron_mass[0]

        lep2_pt = mytree.Electron_pt[1]
        lep2_eta = mytree.Electron_eta[1]
        lep2_phi = mytree.Electron_phi[1]
        lep2_mass = mytree.Electron_mass[1]
        if doFullSel and (lep1_pt < electron_ptmin or lep2_pt < electron_ptmin) :
            continue

    else :

        lep1_pt = mytree.Muon_pt[0]
        lep1_eta = mytree.Muon_eta[0]
        lep1_phi = mytree.Muon_phi[0]
        lep1_mass = mytree.Muon_mass[0]

        lep2_pt = mytree.Electron_pt[0]
        lep2_eta = mytree.Electron_eta[0]
        lep2_phi = mytree.Electron_phi[0]
        lep2_mass = mytree.Electron_mass[0]
        if doFullSel and (lep1_pt < muon_ptmin or lep2_pt < electron_ptmin) :
            continue

    lep1_FourMom.SetPtEtaPhiM(lep1_pt,lep1_eta,lep1_phi,lep1_mass)
    lep2_FourMom.SetPtEtaPhiM(lep2_pt,lep2_eta,lep2_phi,lep2_mass)
    Zcand_FourMom = lep1_FourMom + lep2_FourMom

    if hasattr(mytree, 'Electron_mvaFall17V2Iso_WP80') and not mytree.Electron_mvaFall17V2Iso_WP80[0] :  #FIXME
        continue

    jet_FourMom = ROOT.TLorentzVector()
    njets_25  = 0
    njets_25_dr = 0
    nbjets_25 = 0
    jetptmax  = 0.
    jetbtag   = -2. #btag score for highest pT jet
    jetlep1dr = -1.
    jetlep2dr = -1.
    for jetcount in xrange(mytree.nJet) :

        if mytree.Jet_jetId[jetcount] < jetIdflag :
            continue

        pt_of_jet = mytree.Jet_pt[jetcount]
        jet_FourMom.SetPtEtaPhiM(pt_of_jet, mytree.Jet_eta[jetcount],
                                 mytree.Jet_phi[jetcount], mytree.Jet_mass[jetcount])
#        if pt_of_jet < 50. :    FIXME
#            if mytree.Jet_puId[jetcount] < jetPUIdflag :
#                continue

        if pt_of_jet > 25. :
            jetlep1deltar = lep1_FourMom.DeltaR(jet_FourMom)
            jetlep2deltar = lep2_FourMom.DeltaR(jet_FourMom)
            if pt_of_jet > jetptmax :
                jetptmax = pt_of_jet
                if hasattr(mytree, 'Jet_btagDeepB') :
                    jetbtag = mytree.Jet_btagDeepB[jetcount]
                jetlep1dr = jetlep1deltar
                jetlep2dr = jetlep2deltar
            if jetlep1deltar > 0.3 and jetlep2deltar > 0.3 :
                njets_25_dr = njets_25_dr + 1
            njets_25 = njets_25 + 1
            if hasattr(mytree, 'Jet_btagDeepB') and mytree.Jet_btagDeepB[jetcount] > 0.4184 :
                nbjets_25 = nbjets_25 + 1
        #End jet loop
    if nbjets_25 > 0 and doFullSel :
        continue
    met_pt_puppi = mytree.PuppiMET_pt
    met_sumEt_puppi = mytree.PuppiMET_sumEt

    jetsel = jetptmax < 78.
    metsel = met_pt_puppi < 28.
    select_bool = (jetsel and metsel) or not doFullSel

    if select_bool :
        Nevts_selected = Nevts_selected + 1

    nPV = mytree.PV_npvs

    ############################################################################
    #                                                                          #
    #--------------------- Determine the total event weight -------------------#
    #                                                                          #
    ############################################################################

    #Lepton scale factors
    if not isData :
        if mytree.nMuon == 2 : # Get muon scale factors, which are different for two groups of datasets, and weight them for the respective integrated lumi 

            isSingleMuTrigger_LOW = mytree.HLT_IsoMu24
            if runningEra == 1:
                isSingleMuTrigger_LOW = mytree.HLT_IsoMu27

            lep1_weight = myWF.get_muon_scale(lep1_pt,lep1_eta,isSingleMuTrigger_LOW,runningEra)
            lep2_weight = myWF.get_muon_scale(lep2_pt,lep2_eta,isSingleMuTrigger_LOW,runningEra)

        ############### ELECTRON SFs ##############
        elif mytree.nElectron == 2 :
            lep1_weight = myWF.get_ele_scale(lep1_pt, lep1_eta + mytree.Electron_deltaEtaSC[0],runningEra)
            lep2_weight = myWF.get_ele_scale(lep2_pt, lep2_eta + mytree.Electron_deltaEtaSC[1],runningEra)
        elif mytree.nMuon == 1 :
            isSingleMuTrigger_LOW = mytree.HLT_IsoMu24
            if runningEra == 1:
                isSingleMuTrigger_LOW = mytree.HLT_IsoMu27

            lep1_weight = myWF.get_muon_scale(lep1_pt,lep1_eta,isSingleMuTrigger_LOW,runningEra)
            lep2_weight = myWF.get_ele_scale(lep2_pt, lep2_eta + mytree.Electron_deltaEtaSC[0],runningEra)

        ############### Multiply weights and SFs for MC. Set weight to 1 for data ###############
        MC_Weight = mytree.genWeight
        PU_Weight = 1.
        if hasattr(mytree, 'puWeight') :
            PU_Weight = mytree.puWeight # Add Pile Up weight

        Event_Weight = norm_factor*MC_Weight*PU_Weight/math.fabs(MC_Weight) # Just take the sign of the gen weight
        Event_Weight = Event_Weight*lep1_weight*lep2_weight

    else:
        Event_Weight = 1.

    #Fill the tree variables
    _FourlepMass[0] = Zcand_FourMom.M()
    _met[0]         = met_pt_puppi
    _jetptmax[0]    = jetptmax
    _mcweight[0]    = Event_Weight
    _lep1pt[0]      = lep1_pt
    _lep2pt[0]      = lep2_pt

    if mytree.nMuon == 1 and select_bool:
        Nevts_expected += Event_Weight # Increment the number of events survived in the analyzed sample
   
    ############################################################################
    #                                                                          #
    #------------------------------- Fill histos ------------------------------#
    #                                                                          #
    ############################################################################
    if mytree.nMuon == 1 :
        if select_bool :
            if not isData or (Zcand_FourMom.M() < 84. or Zcand_FourMom.M() > 101.) :
                h_base["h_Mmue"].Fill(Zcand_FourMom.M(),Event_Weight)

            h_base["h_lep1pt"].Fill(lep1_pt,Event_Weight)
            h_base["h_lep1eta"].Fill(lep1_eta,Event_Weight)
            h_base["h_lep1phi"].Fill(lep1_phi,Event_Weight)
            h_base["h_lep2pt"].Fill(lep2_pt,Event_Weight)
            h_base["h_lep2eta"].Fill(lep2_eta,Event_Weight)
            h_base["h_lep2phi"].Fill(lep2_phi,Event_Weight)

            h_base["h_njets25"].Fill(njets_25,Event_Weight)
            h_base["h_njets25dr"].Fill(njets_25_dr,Event_Weight)
            h_base["h_nbjets25"].Fill(nbjets_25,Event_Weight)
            h_base["h_btagid"].Fill(jetbtag,Event_Weight)
            h_base["h_met_sumEt"].Fill(met_sumEt_puppi,Event_Weight)
            h_base["h_jetlep1dr"].Fill(jetlep1dr,Event_Weight)
            h_base["h_jetlep2dr"].Fill(jetlep2dr,Event_Weight)

            h_base["h_npvs"].Fill(nPV,Event_Weight)

            tree_signalreg.Fill()

        if select_bool or (metsel and not select_bool) :
            h_base["h_jetptmax"].Fill(jetptmax,Event_Weight)
        if select_bool or (jetsel and not select_bool) :
            h_base["h_met_pt"].Fill(met_pt_puppi,Event_Weight)
        if jetsel :
            h_base["h_cuts"].Fill(1,Event_Weight)
        if metsel :
            h_base["h_cuts"].Fill(2,Event_Weight)
        if nbjets_25 < 1 :
            h_base["h_cuts"].Fill(3,Event_Weight)

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
