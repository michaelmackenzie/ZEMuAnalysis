mkdir histos
mkdir histos/latest_production

rm histos/latest_production/*2016*.root
rm trees/*2016*.root

python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarToSemiLeptonic_SigRegion_2016.root histos/latest_production/ZEMuHistos_ttbarsemilep_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ttbarlnu_SigRegion_2016.root histos/latest_production/ZEMuHistos_ttbarlnu_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleToptW_SigRegion_2016.root histos/latest_production/ZEMuHistos_SingleToptW_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_SingleAntiToptW_SigRegion_2016.root histos/latest_production/ZEMuHistos_SingleAntiToptW_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_DY50_SigRegion_2016.root histos/latest_production/ZEMuHistos_DY_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WW_SigRegion_2016.root histos/latest_production/ZEMuHistos_WW_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WZ_SigRegion_2016.root histos/latest_production/ZEMuHistos_WZ_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_Wlnu_SigRegion_2016.root histos/latest_production/ZEMuHistos_Wlnu_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WWW_SigRegion_2016.root histos/latest_production/ZEMuHistos_WWW_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich30to40_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich30to40_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich30toInf_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich30toInf_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich40toInf_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich40toInf_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ZZ_SigRegion_2016.root histos/latest_production/ZEMuHistos_ZZ_2016.root

hadd -f trees/ZEMuAnalysis_Background_2016.root histos/latest_production/*2016*.root

python generate_histos.py 0 1 rootfiles/latest_production/MC/signals/ZEMuAnalysis_Signal_2016.root histos/latest_production/ZEMuHistos_Signal_2016.root
cp histos/latest_production/ZEMuHistos_Signal_2016.root trees/ZEMuAnalysis_Signal_2016.root

#Merge samples
hadd histos/latest_production/ZEMuHistos_ttbar_2016.root histos/latest_production/ZEMuHistos_ttbar*_2016.root
rm histos/latest_production/ZEMuHistos_ttbarsemilep_2016.root histos/latest_production/ZEMuHistos_ttbarlnu_2016.root

hadd histos/latest_production/ZEMuHistos_STtW_2016.root histos/latest_production/ZEMuHistos_Single*ToptW_2016.root
rm histos/latest_production/ZEMuHistos_Single*ToptW_2016.root

hadd histos/latest_production/ZEMuHistos_QCD_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEM*_2016.root
rm histos/latest_production/ZEMuHistos_QCDDoubleEM*_2016.root

#Now do the data

python generate_histos.py 0 1 rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleMu_SigRegion_2016.root histos/latest_production/ZEMuHistos_SingleMu_2016.root
python generate_histos.py 0 1 rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleEle_SigRegion_2016.root histos/latest_production/ZEMuHistos_SingleEle_2016.root

hadd histos/latest_production/ZEMuHistos_Data_2016.root histos/latest_production/ZEMuHistos_Single*_2016.root
rm histos/latest_production/ZEMuHistos_SingleMu_2016.root histos/latest_production/ZEMuHistos_SingleEle_2016.root

cp histos/latest_production/ZEMuHistos_Data_2016.root trees/ZEMuHistos_Data_2016.root
