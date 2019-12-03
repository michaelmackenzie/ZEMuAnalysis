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

#------------------------------- Scale factors 2018 ------------------------------#

el_ID_scale_name_2018  = "scale_factors/2018_ElectronMVA90.root"
el_ID_scale_file_2018  = ROOT.TFile(el_ID_scale_name_2018)
el_ID_scale_histo_2018 = ROOT.TH2F()
el_ID_scale_histo_2018 = el_ID_scale_file_2018.Get("EGamma_SF2D")

el_reco_scale_name_2018  = "scale_factors/egammaEffi.txt_EGM2D_updatedAll_2018.root"
el_reco_scale_file_2018  = ROOT.TFile(el_reco_scale_name_2018)
el_reco_scale_histo_2018 = ROOT.TH2F()
el_reco_scale_histo_2018 = el_reco_scale_file_2018.Get("EGamma_SF2D")

mu_ID_scale_name_2018  = "scale_factors/RunABCD_SF_ID_muon_2018.root"
mu_ID_scale_file_2018  = ROOT.TFile(mu_ID_scale_name_2018)
mu_ID_scale_histo_2018 = ROOT.TH2F()
mu_ID_scale_histo_2018 = mu_ID_scale_file_2018.Get("NUM_MediumID_DEN_TrackerMuons_pt_abseta")

mu_Iso_scale_name_2018  = "scale_factors/RunABCD_SF_ISO_muon_2018.root"
mu_Iso_scale_file_2018  = ROOT.TFile(mu_Iso_scale_name_2018)
mu_Iso_scale_histo_2018 = ROOT.TH2F()
mu_Iso_scale_histo_2018 = mu_Iso_scale_file_2018.Get("NUM_LooseRelIso_DEN_MediumID_pt_abseta")

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

        self.norm_filename_2016 = "rootfiles/latest_production/MC/normalizations/Normalizations_table_2016.txt"
        self.norm_filename_2017 = "rootfiles/latest_production/MC/normalizations/Normalizations_table_2017.txt"
        self.norm_filename_2018 = "rootfiles/latest_production/MC/normalizations/Normalizations_table_2018.txt"

    ###############################################################################################################################################

    def get_normalizations_map(self, runningEra):
        #list_dirs_norm = os.listdir(self.dir_norm_input)
        if runningEra == 0:
            in_file = open(self.norm_filename_2016,"r")
        if runningEra == 1:
            in_file = open(self.norm_filename_2017,"r")
        if runningEra == 2:
            in_file = open(self.norm_filename_2018,"r")
        norm_map = dict()

        for line in in_file:
            data_norm = line.split()
            norm_map[data_norm[0]] = float(data_norm[1])

        return norm_map

    ###############################################################################################################################################

    def get_ele_scale(self, lep_pt, lep_eta, runningEra):

        if runningEra == 0: # Scale factors for 2016

            local_lep_pt = lep_pt
            if local_lep_pt > 150.: # This is because corrections are up to 150 GeV
                local_lep_pt = 150.

            local_lep_eta = lep_eta
            if local_lep_eta >= 2.5:
                local_lep_eta = 2.49
            if local_lep_eta <= -2.5:
                local_lep_eta = -2.49


            scale_factor_ID   = el_ID_scale_histo_2016.GetBinContent( el_ID_scale_histo_2016.GetXaxis().FindBin(local_lep_eta), el_ID_scale_histo_2016.GetYaxis().FindBin(local_lep_pt) )
            scale_factor = scale_factor_ID

        elif runningEra == 1: # Scale factors for 2017

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
            scale_factor = scale_factor_ID * scale_factor_reco

        elif runningEra == 2: # Scale factors for 2018

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
            scale_factor = scale_factor_ID * scale_factor_reco

        return scale_factor

    ###############################################################################################################################################

    def get_muon_scale(self, lep_pt, lep_eta, isSingleMuTrigger_LOW, runningEra):

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


        ###############################################
        #                                             #
        #------------ Get muon SF for 2016 -----------#
        #                                             #
        ###############################################

        if runningEra == 0:

            luminosity_norm = 35.86
            luminosity_BtoF = 19.72 #For 2016
            luminosity_GH   = 16.14 #For 2016

            # Use a random number to select which muon scale factor to use, depending on the respective lumi fraction (only for 2016)
            Nrandom_for_SF = ROOT.TRandom3(44317).Rndm()
            
            if Nrandom_for_SF <= (luminosity_BtoF/luminosity_norm): # Access muon SF: B to F

                scale_factor_ID       = mu_ID_scale_histo_BCDEF_2016.GetBinContent( mu_ID_scale_histo_BCDEF_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_ID_scale_histo_BCDEF_2016.GetYaxis().FindBin(local_lep_pt) )
                scale_factor_Iso      = mu_Iso_scale_histo_BCDEF_2016.GetBinContent( mu_Iso_scale_histo_BCDEF_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Iso_scale_histo_BCDEF_2016.GetYaxis().FindBin(local_lep_pt) )

                if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 26 GeV
                    if local_lep_pt_forTrigger < 26.:
                        local_lep_pt_forTrigger = 26.

                    scale_factor_Trigger = mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetBinContent( mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_BCDEF_Mu24_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                    
                    scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

                else: # An event can have more than one trigger

                    local_lep_pt_forTrigger = lep_pt # Corrections related to this trigger start from 52 GeV
                    if local_lep_pt_forTrigger < 52.:
                        local_lep_pt_forTrigger = 52.

                    scale_factor_Trigger = mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetBinContent( mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetXaxis().FindBin(math.fabs(lep_eta)), mu_Trigger_scale_histo_BCDEF_Mu50_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                    scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

            else: #Use GH SFs

                scale_factor_ID       = mu_ID_scale_histo_GH_2016.GetBinContent( mu_ID_scale_histo_GH_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_ID_scale_histo_GH_2016.GetYaxis().FindBin(local_lep_pt) )
                scale_factor_Iso      = mu_Iso_scale_histo_GH_2016.GetBinContent( mu_Iso_scale_histo_GH_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Iso_scale_histo_GH_2016.GetYaxis().FindBin(local_lep_pt) )

                if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                    local_lep_pt_forTrigger = lep_pt 
                    if local_lep_pt_forTrigger < 26.:
                        local_lep_pt_forTrigger = 26.

                    scale_factor_Trigger = mu_Trigger_scale_histo_GH_Mu24_2016.GetBinContent( mu_Trigger_scale_histo_GH_Mu24_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_GH_Mu24_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                    scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

                else: # An event can have more than one trigger

                    local_lep_pt_forTrigger = lep_pt 
                    if local_lep_pt_forTrigger < 52.:
                        local_lep_pt_forTrigger = 52.

                    scale_factor_Trigger = mu_Trigger_scale_histo_GH_Mu50_2016.GetBinContent( mu_Trigger_scale_histo_GH_Mu50_2016.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_GH_Mu50_2016.GetYaxis().FindBin(local_lep_pt_forTrigger) )
                    scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

        ###############################################
        #                                             #
        #------------ Get muon SF for 2017 -----------#
        #                                             #
        ###############################################


        elif runningEra == 1: # Get muon SFs for 2017. ID and ISO histos have pT and eta positions inverted wrt 2016 histos
                              
            scale_factor_ID       = mu_ID_scale_histo_2017.GetBinContent( mu_ID_scale_histo_2017.GetXaxis().FindBin(local_lep_pt), mu_ID_scale_histo_2017.GetYaxis().FindBin(math.fabs(local_lep_eta)) )
            scale_factor_Iso      = mu_Iso_scale_histo_2017.GetBinContent( mu_Iso_scale_histo_2017.GetXaxis().FindBin(local_lep_pt), mu_Iso_scale_histo_2017.GetYaxis().FindBin(math.fabs(local_lep_eta)) )

            if isSingleMuTrigger_LOW: # Trigger SF go up to higher energies than 120 GeV, so no local_lep_pt is used for those

                local_lep_pt_forTrigger = lep_pt 
                if local_lep_pt_forTrigger < 29.:
                    local_lep_pt_forTrigger = 29.

                scale_factor_Trigger = mu_Trigger_scale_histo_2017_Mu27.GetBinContent( mu_Trigger_scale_histo_2017_Mu27.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_2017_Mu27.GetYaxis().FindBin(local_lep_pt_forTrigger) )

            else: # An event can have more than one trigger

                local_lep_pt_forTrigger = lep_pt 
                if local_lep_pt_forTrigger < 52.:
                    local_lep_pt_forTrigger = 52.

                scale_factor_Trigger = mu_Trigger_scale_histo_2017_Mu50.GetBinContent( mu_Trigger_scale_histo_2017_Mu50.GetXaxis().FindBin(math.fabs(local_lep_eta)), mu_Trigger_scale_histo_2017_Mu50.GetYaxis().FindBin(local_lep_pt_forTrigger) )

                
            scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

        ###############################################
        #                                             #
        #------------ Get muon SF for 2018 -----------#
        #                                             #
        ###############################################

        elif runningEra == 2:

            luminosity_norm = 59.69
            luminosity_BeforeHLTUpdate = 8.98
            luminosity_AfterHLTUpdate = 50.71

            # Use a random number to select which muon scale factor to use for trigger, depending on the respective lumi fraction (only for 2018)
            Nrandom_for_SF = ROOT.TRandom3(92562).Rndm()
            
            scale_factor_ID       = mu_ID_scale_histo_2018.GetBinContent( mu_ID_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_ID_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )
            scale_factor_Iso      = mu_Iso_scale_histo_2018.GetBinContent( mu_Iso_scale_histo_2018.GetXaxis().FindBin(local_lep_pt), mu_Iso_scale_histo_2018.GetYaxis().FindBin(math.fabs(local_lep_eta)) )

            if Nrandom_for_SF <= (luminosity_BeforeHLTUpdate/luminosity_norm): # Access muon Trigger SF: Before HLT Update

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

            else: # Access muon Trigger SF: After HLT Update

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


            scale_factor         = scale_factor_ID * scale_factor_Iso * scale_factor_Trigger

        return scale_factor
