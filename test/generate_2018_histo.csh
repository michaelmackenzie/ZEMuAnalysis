mkdir histos
mkdir histos/latest_production

rm histos/latest_production/*2018*.root
rm trees/*2018*.root
doFullSel=0 #0 or 1
channel=0 #0 = emu, 1 = mutau, 2 = etau

echo "Running selections for channel " ${channel} " with doFullSel =" ${doFullSel}

python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_DY50_SigRegion_2018.root histos/latest_production/ZEMuHistos_DY_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleAntiToptW_SigRegion_2018.root histos/latest_production/ZEMuHistos_SingleAntiToptW_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleToptW_SigRegion_2018.root histos/latest_production/ZEMuHistos_SingleToptW_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WW_SigRegion_2018.root histos/latest_production/ZEMuHistos_WW_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WZ_SigRegion_2018.root histos/latest_production/ZEMuHistos_WZ_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarlnu_SigRegion_2018.root histos/latest_production/ZEMuHistos_ttbarlnu_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarToSemiLeptonic_SigRegion_2018.root histos/latest_production/ZEMuHistos_ttbar_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_Wlnu_SigRegion_2018.root histos/latest_production/ZEMuHistos_Wlnu_2018.root ${channel}

hadd -f trees/ZEMuAnalysis_Background_2018.root histos/latest_production/*2018*.root

python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/MC/signals/ZEMuAnalysis_Signal_2018.root histos/latest_production/ZEMuHistos_Signal_2018.root ${channel}

cp histos/latest_production/ZEMuHistos_Signal_2018.root trees/ZEMuAnalysis_Signal_2018.root

# #Merge samples
hadd histos/latest_production/ZEMuHistos_STtW_2018.root histos/latest_production/ZEMuHistos_Single*ToptW_2018.root
rm histos/latest_production/ZEMuHistos_Single*ToptW_2018.root

#Now do the data

python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleMu_SigRegion_2018.root histos/latest_production/ZEMuHistos_SingleMu_2018.root ${channel}
python generate_histos.py 2 ${doFullSel} rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleEle_SigRegion_2018.root histos/latest_production/ZEMuHistos_SingleEle_2018.root ${channel}

hadd histos/latest_production/ZEMuHistos_Data_2018.root histos/latest_production/ZEMuHistos_Single*_2018.root
rm histos/latest_production/ZEMuHistos_SingleMu_2018.root histos/latest_production/ZEMuHistos_SingleEle_2018.root

cp histos/latest_production/ZEMuHistos_Data_2018.root trees/ZEMuHistos_Data_2018.root
