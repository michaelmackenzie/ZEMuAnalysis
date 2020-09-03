import ROOT
import math
import os
from array import array

###################################################################################
#                                                                                 #
#----------- Acess scale factor histos for EGamma and Muon corrections -----------#
#                                                                                 #
#        https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaIDRecipesRun2         #
#   https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2016LegacyRereco    #
#                                                                                 #
###################################################################################

#------------------------------- Scale factors 2016 ------------------------------#

el_ID_scale_name_2016  = "scale_factors/2016LegacyReReco_ElectronMVAwp80.root"
el_ID_scale_file_2016  = ROOT.TFile(el_ID_scale_name_2016)
el_ID_scale_histo_2016 = ROOT.TH2F()
el_ID_scale_histo_2016 = el_ID_scale_file_2016.Get("EGamma_SF2D")

el_reco_scale_name_2016  = "scale_factors/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root"
el_reco_scale_file_2016  = ROOT.TFile(el_reco_scale_name_2016)
el_reco_scale_histo_2016 = ROOT.TH2F()
el_reco_scale_histo_2016 = el_reco_scale_file_2016.Get("EGamma_SF2D")

el_trigger_scale_name_2016  = "scale_factors/egammaTriggerEfficiency_2016.root"
el_trigger_scale_file_2016  = ROOT.TFile(el_trigger_scale_name_2016)
el_trigger_scale_histo_2016 = ROOT.TH2F()
el_trigger_scale_histo_2016 = el_trigger_scale_file_2016.Get("EGamma_SF2D")

mu_ID_scale_name_BCDEF_2016  = "scale_factors/RunBCDEF_SF_ID_muon_2016.root"
mu_ID_scale_file_BCDEF_2016  = ROOT.TFile(mu_ID_scale_name_BCDEF_2016)
mu_ID_scale_histo_BCDEF_2016 = ROOT.TH2F()
mu_ID_scale_histo_BCDEF_2016 = mu_ID_scale_file_BCDEF_2016.Get("NUM_TightID_DEN_genTracks_eta_pt")

mu_ID_scale_name_GH_2016  = "scale_factors/RunGH_SF_ID_muon_2016.root"
mu_ID_scale_file_GH_2016  = ROOT.TFile(mu_ID_scale_name_GH_2016)
mu_ID_scale_histo_GH_2016 = ROOT.TH2F()
mu_ID_scale_histo_GH_2016 = mu_ID_scale_file_GH_2016.Get("NUM_TightID_DEN_genTracks_eta_pt")

mu_Iso_scale_name_BCDEF_2016  = "scale_factors/RunBCDEF_SF_ISO_muon_2016.root"
mu_Iso_scale_file_BCDEF_2016  = ROOT.TFile(mu_Iso_scale_name_BCDEF_2016)
mu_Iso_scale_histo_BCDEF_2016 = ROOT.TH2F()
mu_Iso_scale_histo_BCDEF_2016 = mu_Iso_scale_file_BCDEF_2016.Get("NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt")

mu_Iso_scale_name_GH_2016  = "scale_factors/RunGH_SF_ISO_muon_2016.root"
mu_Iso_scale_file_GH_2016  = ROOT.TFile(mu_Iso_scale_name_GH_2016)
mu_Iso_scale_histo_GH_2016 = ROOT.TH2F()
mu_Iso_scale_histo_GH_2016 = mu_Iso_scale_file_GH_2016.Get("NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt")

mu_Trigger_scale_name_BCDEF_2016       = "scale_factors/EfficienciesAndSF_RunBtoF_muon_2016.root"
mu_Trigger_scale_file_BCDEF_2016       = ROOT.TFile(mu_Trigger_scale_name_BCDEF_2016)
mu_Trigger_scale_histo_BCDEF_Mu24_2016 = ROOT.TH2F()
mu_Trigger_scale_histo_BCDEF_Mu24_2016 = mu_Trigger_scale_file_BCDEF_2016.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_BCDEF_Mu50_2016 = ROOT.TH2F()
mu_Trigger_scale_histo_BCDEF_Mu50_2016 = mu_Trigger_scale_file_BCDEF_2016.Get("Mu50_OR_TkMu50_PtEtaBins/abseta_pt_ratio")

mu_Trigger_scale_name_GH_2016       = "scale_factors/EfficienciesAndSF_Period4_muonTrigger_2016.root"
mu_Trigger_scale_file_GH_2016       = ROOT.TFile(mu_Trigger_scale_name_GH_2016)
mu_Trigger_scale_histo_GH_Mu24_2016 = ROOT.TH2F()
mu_Trigger_scale_histo_GH_Mu24_2016 = mu_Trigger_scale_file_GH_2016.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_GH_Mu50_2016 = ROOT.TH2F()
mu_Trigger_scale_histo_GH_Mu50_2016 = mu_Trigger_scale_file_GH_2016.Get("Mu50_OR_TkMu50_PtEtaBins/abseta_pt_ratio")

#------------------------------- Scale factors 2017 ------------------------------#

el_ID_scale_name_2017  = "scale_factors/2017_ElectronMVA80.root"
el_ID_scale_file_2017  = ROOT.TFile(el_ID_scale_name_2017)
el_ID_scale_histo_2017 = ROOT.TH2F()
el_ID_scale_histo_2017 = el_ID_scale_file_2017.Get("EGamma_SF2D")

el_reco_scale_name_2017  = "scale_factors/egammaEffi.txt_EGM2D_runBCDEF_passingRECO_2017.root"
el_reco_scale_file_2017  = ROOT.TFile(el_reco_scale_name_2017)
el_reco_scale_histo_2017 = ROOT.TH2F()
el_reco_scale_histo_2017 = el_reco_scale_file_2017.Get("EGamma_SF2D")

el_trigger_scale_name_2017  = "scale_factors/egammaTriggerEfficiency_2017.root"
el_trigger_scale_file_2017  = ROOT.TFile(el_trigger_scale_name_2017)
el_trigger_scale_histo_2017 = ROOT.TH2F()
el_trigger_scale_histo_2017 = el_trigger_scale_file_2017.Get("EGamma_SF2D")

mu_ID_scale_name_2017  = "scale_factors/2017_Mu_RunBCDEF_SF_ID.root"
mu_ID_scale_file_2017  = ROOT.TFile(mu_ID_scale_name_2017)
mu_ID_scale_histo_2017 = ROOT.TH2F()
mu_ID_scale_histo_2017 = mu_ID_scale_file_2017.Get("NUM_TightID_DEN_genTracks_pt_abseta")

mu_Iso_scale_name_2017  = "scale_factors/2017_Mu_RunBCDEF_SF_ISO.root"
mu_Iso_scale_file_2017  = ROOT.TFile(mu_Iso_scale_name_2017)
mu_Iso_scale_histo_2017 = ROOT.TH2F()
mu_Iso_scale_histo_2017 = mu_Iso_scale_file_2017.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")

mu_Trigger_scale_name_2017       = "scale_factors/EfficienciesAndSF_2017_RunBtoF_Nov17Nov2017.root"
mu_Trigger_scale_file_2017       = ROOT.TFile(mu_Trigger_scale_name_2017)
mu_Trigger_scale_histo_Mu27_2017 = ROOT.TH2F()
mu_Trigger_scale_histo_Mu27_2017 = mu_Trigger_scale_file_2017.Get("IsoMu27_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_Mu50_2017 = ROOT.TH2F()
mu_Trigger_scale_histo_Mu50_2017 = mu_Trigger_scale_file_2017.Get("Mu50_PtEtaBins/abseta_pt_ratio")

#------------------------------- Scale factors 2018 ------------------------------#

el_ID_scale_name_2018  = "scale_factors/2018_ElectronMVA80.root"
el_ID_scale_file_2018  = ROOT.TFile(el_ID_scale_name_2018)
el_ID_scale_histo_2018 = ROOT.TH2F()
el_ID_scale_histo_2018 = el_ID_scale_file_2018.Get("EGamma_SF2D")

el_reco_scale_name_2018  = "scale_factors/egammaEffi.txt_EGM2D_updatedAll_2018.root"
el_reco_scale_file_2018  = ROOT.TFile(el_reco_scale_name_2018)
el_reco_scale_histo_2018 = ROOT.TH2F()
el_reco_scale_histo_2018 = el_reco_scale_file_2018.Get("EGamma_SF2D")

el_trigger_scale_name_2018  = "scale_factors/egammaTriggerEfficiency_2018.root"
el_trigger_scale_file_2018  = ROOT.TFile(el_trigger_scale_name_2018)
el_trigger_scale_histo_2018 = ROOT.TH2F()
el_trigger_scale_histo_2018 = el_trigger_scale_file_2018.Get("EGamma_SF2D")

mu_ID_scale_name_2018  = "scale_factors/RunABCD_SF_ID_muon_2018.root"
mu_ID_scale_file_2018  = ROOT.TFile(mu_ID_scale_name_2018)
mu_ID_scale_histo_2018 = ROOT.TH2F()
mu_ID_scale_histo_2018 = mu_ID_scale_file_2018.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")

mu_Iso_scale_name_2018  = "scale_factors/RunABCD_SF_ISO_muon_2018.root"
mu_Iso_scale_file_2018  = ROOT.TFile(mu_Iso_scale_name_2018)
mu_Iso_scale_histo_2018 = ROOT.TH2F()
mu_Iso_scale_histo_2018 = mu_Iso_scale_file_2018.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")

mu_Trigger_scale_name_BeforeHLTUpdate_2018       = "scale_factors/EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root"
mu_Trigger_scale_file_BeforeHLTUpdate_2018       = ROOT.TFile(mu_Trigger_scale_name_BeforeHLTUpdate_2018)
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24 = ROOT.TH2F()
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24 = mu_Trigger_scale_file_BeforeHLTUpdate_2018.Get("IsoMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50 = ROOT.TH2F()
mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50 = mu_Trigger_scale_file_BeforeHLTUpdate_2018.Get("Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio")

mu_Trigger_scale_name_AfterHLTUpdate_2018       = "scale_factors/EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root"
mu_Trigger_scale_file_AfterHLTUpdate_2018       = ROOT.TFile(mu_Trigger_scale_name_AfterHLTUpdate_2018)
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24 = ROOT.TH2F()
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24 = mu_Trigger_scale_file_AfterHLTUpdate_2018.Get("IsoMu24_PtEtaBins/abseta_pt_ratio")
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50 = ROOT.TH2F()
mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50 = mu_Trigger_scale_file_AfterHLTUpdate_2018.Get("Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio")


class Simplified_Workflow_Handler:

    def __init__(self,runningEra):

        if runningEra == 0:
            year = "2016"
        if runningEra == 1:
            year = "2017"
        if runningEra == 2:
            year = "2018"

        # Where the files are
        self.dir_bkg_input  = "rootfiles/latest_production/MC/backgrounds/"
        self.dir_sig_input  = "rootfiles/latest_production/MC/signals/"
        self.dir_data_input = "rootfiles/latest_production/dataprocess/"

    ###############################################################################################################################################

    def get_normalizations_map(self, runningEra):
        #list_dirs_norm = os.listdir(self.dir_norm_input)
        if runningEra == 0:
            in_file = open("rootfiles/latest_production/MC/normalizations/Normalizations_table_2016.txt","r")
        if runningEra == 1:
            in_file = open("rootfiles/latest_production/MC/normalizations/Normalizations_table_2017.txt","r")
        if runningEra == 2:
            in_file = open("rootfiles/latest_production/MC/normalizations/Normalizations_table_2018.txt","r")
        norm_map = dict()

        for line in in_file:
            data_norm = line.split()
            norm_map[data_norm[0]] = float(data_norm[1])

        return norm_map

    ###############################################################################################################################################

    def get_ele_scale(self, lep_pt, lep_eta, runningEra, isMuTrigger):

        scale_factor_trigger = 1.

        if runningEra == 0: # Scale factors for 2016

            local_lep_pt = lep_pt
            if local_lep_pt > 150.: # This is because corrections are up to 150 GeV
                local_lep_pt = 150.

            local_lep_pt_4reco = lep_pt
            if local_lep_pt_4reco > 499.:
                local_lep_pt_4reco = 499.

            local_lep_eta = lep_eta
            if local_lep_eta >= 2.5:
                local_lep_eta = 2.49
            if local_lep_eta <= -2.5:
                local_lep_eta = -2.49


            scale_factor_ID   = el_ID_scale_histo_2016.GetBinContent( el_ID_scale_histo_2016.GetXaxis().FindBin(local_lep_eta), el_ID_scale_histo_2016.GetYaxis().FindBin(local_lep_pt) )
            scale_factor_reco   = el_reco_scale_histo_2016.GetBinContent( el_reco_scale_histo_2016.GetXaxis().FindBin(local_lep_eta), el_reco_scale_histo_2016.GetYaxis().FindBin(local_lep_pt_4reco) )
            if not isMuTrigger:
                scale_factor_trigger   = el_trigger_scale_histo_2016.GetBinContent( el_trigger_scale_histo_2016.GetXaxis().FindBin(local_lep_eta), el_trigger_scale_histo_2016.GetYaxis().FindBin(local_lep_pt_4reco) ) #trigger SFs have the same pT maximum of reco SFs
            
        if runningEra == 1: # Scale factors for 2017

            local_lep_pt = lep_pt
            if local_lep_pt > 499.: # This is because corrections are up to 499 GeV
                local_lep_pt = 499.

            local_lep_eta = lep_eta
            if local_lep_eta >= 2.5:
                local_lep_eta = 2.49
            if local_lep_eta < -2.5: # Corrections reach down to eta = -2.5, but only up to eta = 2.49
                local_lep_eta = -2.5

            scale_factor_ID   = el_ID_scale_histo_2017.GetBinContent( el_ID_scale_histo_2017.GetXaxis().FindBin(local_lep_eta), el_ID_scale_histo_2017.GetYaxis().FindBin(local_lep_pt) )
            scale_factor_reco   = el_reco_scale_histo_2017.GetBinContent( el_reco_scale_histo_2017.GetXaxis().FindBin(local_lep_eta), el_reco_scale_histo_2017.GetYaxis().FindBin(local_lep_pt) )
            if not isMuTrigger: 
                scale_factor_trigger   = el_trigger_scale_histo_2017.GetBinContent( el_trigger_scale_histo_2017.GetXaxis().FindBin(local_lep_eta), el_trigger_scale_histo_2017.GetYaxis().FindBin(local_lep_pt) ) #trigger SFs have the same pT maximum of reco SFs

        if runningEra == 2: # Scale factors for 2018

            local_lep_pt = lep_pt
            if local_lep_pt > 499.: # This is because corrections are up to 499 GeV
                local_lep_pt = 499.

            local_lep_eta = lep_eta
            if local_lep_eta >= 2.5:
                local_lep_eta = 2.49
            if local_lep_eta < -2.5: # Corrections reach down to eta = -2.5, but only up to eta = 2.49
                local_lep_eta = -2.5
            
            scale_factor_ID   = el_ID_scale_histo_2018.GetBinContent( el_ID_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_ID_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) )
            scale_factor_reco   = el_reco_scale_histo_2018.GetBinContent( el_reco_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_reco_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) )
            if not isMuTrigger: 
                scale_factor_trigger   = el_trigger_scale_histo_2018.GetBinContent( el_trigger_scale_histo_2018.GetXaxis().FindBin(local_lep_eta), el_trigger_scale_histo_2018.GetYaxis().FindBin(local_lep_pt) ) #trigger SFs have the same pT maximum of reco SFs
            

        return scale_factor_ID * scale_factor_reco * scale_factor_trigger

    ###############################################################################################################################################

    def get_muon_scale(self, lep_pt, lep_eta, isSingleMuTrigger_LOW, runningEra, isMuTrigger):

        local_lep_pt = lep_pt
        if local_lep_pt >= 120.:  # This is because corrections go up to 120 GeV (excluded)
            local_lep_pt = 119.
        if local_lep_pt < 20.:
            local_lep_pt = 20.

        local_lep_eta = lep_eta
        if local_lep_eta >= 2.4:
            local_lep_eta = 2.39
        if local_lep_eta <= -2.4:
            local_lep_eta = -2.39

        scale_factor_Trigger = 1.

        ###############################################
        #                                             #
        #------------ Get muon SF for 2016 -----------#
        #                                             #
        ###############################################

        if runningEra == 0:

            luminosity_norm = 35.92
            luminosity_BtoF = 19.72 #For 2016
            luminosity_GH   = 16.14 #For 2016

            # Use a random number to select which muon scale factor to use, depending on the respective lumi fraction (only for 2016)
            Nrandom_for_SF = ROOT.TRandom3(44317).Rndm()
            
            if Nrandom_for_SF <= (luminosity_BtoF/luminosity_norm): # Access muon SF: B to F

                scale_factor_ID       = mu_ID_scale_histo_BCDEF_2016.GetBinContent( mu_ID_scale_histo_BCDEF_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_ID_scale_histo_BCDEF_2016.GetYaxis().FindBin(local_lep_pt) )
                scale_factor_Iso      = mu_Iso_scale_histo_BCDEF_2016.GetBinContent( mu_Iso_scale_histo_BCDEF_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Iso_scale_histo_BCDEF_2016.GetYaxis().FindBin(local_lep_pt) )

                if isMuTrigger: 
                    if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                        local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 26 GeV
                        if local_lep_pt_forTrigger < 26.:
                            local_lep_pt_forTrigger = 26.

                        scale_factor_Trigger = mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetBinContent( mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                    
                    else: # An event can have more than one trigger

                        local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV
                        if local_lep_pt_forTrigger < 52.:
                            local_lep_pt_forTrigger = 52.

                        scale_factor_Trigger = mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetBinContent( mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetXaxis().FindBin(math.fabs(lep_eta)), mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                    
            else: #Use GH SFs

                scale_factor_ID       = mu_ID_scale_histo_GH_2016.GetBinContent( mu_ID_scale_histo_GH_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_ID_scale_histo_GH_2016.GetYaxis().FindBin(local_lep_pt) )
                scale_factor_Iso      = mu_Iso_scale_histo_GH_2016.GetBinContent( mu_Iso_scale_histo_GH_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Iso_scale_histo_GH_2016.GetYaxis().FindBin(local_lep_pt) )

                if isMuTrigger:
                    if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                        local_lep_pt_forTrigger = lep_pt 
                        if local_lep_pt_forTrigger < 26.:
                            local_lep_pt_forTrigger = 26.

                        scale_factor_Trigger = mu_Trigger_scale_histo_GH_Mu24_2016.GetBinContent( mu_Trigger_scale_histo_GH_Mu24_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_GH_Mu24_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                    else: # An event can have more than one trigger

                        local_lep_pt_forTrigger = lep_pt 
                        if local_lep_pt_forTrigger < 52.:
                            local_lep_pt_forTrigger = 52.

                        scale_factor_Trigger = mu_Trigger_scale_histo_GH_Mu50_2016.GetBinContent( mu_Trigger_scale_histo_GH_Mu50_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_GH_Mu50_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )

            scale_factor = scale_factor_ID * scale_factor_Trigger * scale_factor_Iso 

        ###############################################
        #                                             #
        #------------ Get muon SF for 2017 -----------#
        #                                             #
        ###############################################


        if runningEra == 1: # Get muon SFs for 2017. ID and ISO histos have pT and eta positions inverted wrt 2016 histos
                              
            scale_factor_ID       = mu_ID_scale_histo_2017.GetBinContent( mu_ID_scale_histo_2017.GetXaxis().FindBin(local_lep_pt), mu_ID_scale_histo_2017.GetYaxis().FindBin(math.fabs(local_lep_eta)) )
            scale_factor_Iso      = mu_Iso_scale_histo_2017.GetBinContent( mu_Iso_scale_histo_2017.GetXaxis().FindBin(local_lep_pt), mu_Iso_scale_histo_2017.GetYaxis().FindBin(math.fabs(local_lep_eta)) )

            if isMuTrigger:
                if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt 
                    if local_lep_pt_forTrigger < 29.:
                        local_lep_pt_forTrigger = 29.
                    scale_factor_Trigger = mu_Trigger_scale_histo_Mu27_2017.GetBinContent( mu_Trigger_scale_histo_Mu27_2017.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_Mu27_2017.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                else: # An event can have more than one trigger

                    local_lep_pt_forTrigger = lep_pt 
                    if local_lep_pt_forTrigger < 52.:
                        local_lep_pt_forTrigger = 52.
                    scale_factor_Trigger = mu_Trigger_scale_histo_Mu50_2017.GetBinContent( mu_Trigger_scale_histo_Mu50_2017.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_Mu50_2017.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                
            scale_factor  = scale_factor_ID * scale_factor_Trigger * scale_factor_Iso 

        ###############################################
        #                                             #
        #------------ Get muon SF for 2018 -----------#
        #                                             #
        ###############################################

        if runningEra == 2:

            luminosity_norm = 59.74
            luminosity_BeforeHLTUpdate = 8.98
            luminosity_AfterHLTUpdate = 50.71

            # Use a random number to select which muon scale factor to use for trigger, depending on the respective lumi fraction (only for 2018)
            Nrandom_for_SF = ROOT.TRandom3(92562).Rndm()
            
            scale_factor_ID       = mu_ID_scale_histo_2018.GetBinContent( mu_ID_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_ID_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )
            scale_factor_Iso      = mu_Iso_scale_histo_2018.GetBinContent( mu_Iso_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_Iso_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )

            if Nrandom_for_SF <= (luminosity_BeforeHLTUpdate/luminosity_norm) and isMuTrigger: # Access muon Trigger SF: Before HLT Update

                if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 26 GeV
                    if local_lep_pt_forTrigger < 26.:
                        local_lep_pt_forTrigger = 26.

                    scale_factor_Trigger = mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24.GetBinContent( mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu24.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                else: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV
                    if local_lep_pt_forTrigger < 52.:
                        local_lep_pt_forTrigger = 52.
                
                    scale_factor_Trigger = mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetBinContent( mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_BeforeHLTUpdate_2018_Mu50.GetYaxis().FindBin(local_lep_pt_forTrigger) )

            elif isMuTrigger: # Access muon Trigger SF: After HLT Update

                if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 26 GeV
                    if local_lep_pt_forTrigger < 26.:
                        local_lep_pt_forTrigger = 26.

                    scale_factor_Trigger = mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24.GetBinContent( mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu24.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                else: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV
                    if local_lep_pt_forTrigger < 52.:
                        local_lep_pt_forTrigger = 52.
                
                    scale_factor_Trigger = mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetBinContent( mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_AfterHLTUpdate_2018_Mu50.GetYaxis().FindBin(local_lep_pt_forTrigger) )

            scale_factor = scale_factor_ID * scale_factor_Trigger * scale_factor_Iso 

        return scale_factor
