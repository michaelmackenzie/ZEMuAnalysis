mkdir histos
mkdir histos/latest_production

rm histos/latest_production/*2017*.root
rm trees/*2017*.root
doFullSel=0 #0 or 1
channel=0 #0 = emu, 1 = mutau, 2 = etau

echo "Running selections for channel " ${channel} " with doFullSel =" ${doFullSel}

python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_DY50_SigRegion_2017.root histos/latest_production/ZEMuHistos_DY_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleAntiToptW_SigRegion_2017.root histos/latest_production/ZEMuHistos_SingleAntiToptW_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleToptW_SigRegion_2017.root histos/latest_production/ZEMuHistos_SingleToptW_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WW_SigRegion_2017.root histos/latest_production/ZEMuHistos_WW_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WZ_SigRegion_2017.root histos/latest_production/ZEMuHistos_WZ_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarlnu_SigRegion_2017.root histos/latest_production/ZEMuHistos_ttbarlnu_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarToSemiLeptonic_SigRegion_2017.root histos/latest_production/ZEMuHistos_ttbar_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_Wlnu_SigRegion_2017.root histos/latest_production/ZEMuHistos_Wlnu_2017.root ${channel}

hadd -f trees/ZEMuAnalysis_Background_2017.root histos/latest_production/*2017*.root

python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/MC/signals/ZEMuAnalysis_Signal_2017.root histos/latest_production/ZEMuHistos_Signal_2017.root ${channel}

cp histos/latest_production/ZEMuHistos_Signal_2017.root trees/ZEMuAnalysis_Signal_2017.root

# #Merge samples
hadd histos/latest_production/ZEMuHistos_STtW_2017.root histos/latest_production/ZEMuHistos_Single*ToptW_2017.root
rm histos/latest_production/ZEMuHistos_Single*ToptW_2017.root

#Now do the data

python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleMu_SigRegion_2017.root histos/latest_production/ZEMuHistos_SingleMu_2017.root ${channel}
python generate_histos.py 1 ${doFullSel} rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleEle_SigRegion_2017.root histos/latest_production/ZEMuHistos_SingleEle_2017.root ${channel}

hadd histos/latest_production/ZEMuHistos_Data_2017.root histos/latest_production/ZEMuHistos_Single*_2017.root
rm histos/latest_production/ZEMuHistos_SingleMu_2017.root histos/latest_production/ZEMuHistos_SingleEle_2017.root

cp histos/latest_production/ZEMuHistos_Data_2017.root trees/ZEMuHistos_Data_2017.root
