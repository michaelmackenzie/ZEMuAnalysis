mkdir trees
mkdir histos
mkdir histos/latest_production

rm histos/latest_production/*2016*.root
rm trees/*2016*.root
doFullSel=0 #0 or 1
channel=0 #0 = emu, 1 = etau, 2 = mutau

<<<<<<< HEAD
outdir="emu"
if [ $channel -eq 1 ]
then
    outdir="etau"
elif [ $channel -eq 2 ]
then
    outdir="mutau"
fi
# python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_WWW_SigRegion_2016.root histos/latest_production/ZEMuHistos_WWW_2016.root
# python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich30to40_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich30to40_2016.root
# python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich30toInf_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich30toInf_2016.root
# python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_QCDDoubleEMEnrich40toInf_SigRegion_2016.root histos/latest_production/ZEMuHistos_QCDDoubleEMEnrich40toInf_2016.root
# python generate_histos.py 0 1 rootfiles/latest_production/MC/backgrounds/ZEMuAnalysis_ZZ_SigRegion_2016.root histos/latest_production/ZEMuHistos_ZZ_2016.root

echo "Running selections for channel " ${channel} " = " ${outdir} "  with doFullSel =" ${doFullSel}

outdir="histos/latest_production/"${outdir}

if [ ! -d ${outdir} ]
then
    mkdir ${outdir}
fi

python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_DY50_2016.root ${outdir}/LFVHistos_DY_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_SingleAntiToptW_2016.root ${outdir}/LFVHistos_SingleAntiToptW_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_SingleToptW_2016.root ${outdir}/LFVHistos_SingleToptW_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_WW_2016.root ${outdir}/LFVHistos_WW_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_WZ_2016.root ${outdir}/LFVHistos_WZ_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_ttbarlnu_2016.root ${outdir}/LFVHistos_ttbarlnu_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_ttbarToSemiLeptonic_2016.root ${outdir}/LFVHistos_ttbar_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/backgrounds/LFVAnalysis_Wlnu_2016.root ${outdir}/LFVHistos_Wlnu_2016.root ${channel}

hadd -f trees/LFVAnalysis_Background_2016.root ${outdir}/*2016*.root

python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_ZEMu_2016.root ${outdir}/LFVHistos_ZEMu_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_ZETau_2016.root ${outdir}/LFVHistos_ZETau_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_ZMuTau_2016.root ${outdir}/LFVHistos_ZMuTau_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_HEMu_2016.root ${outdir}/LFVHistos_HEMu_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_HETau_2016.root ${outdir}/LFVHistos_HETau_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/MC/signals/LFVAnalysis_HMuTau_2016.root ${outdir}/LFVHistos_HMuTau_2016.root ${channel}

cp ${outdir}/LFVHistos_ZEMu_2016.root trees/LFVAnalysis_ZEMu_2016.root
cp ${outdir}/LFVHistos_ZETau_2016.root trees/LFVAnalysis_ZETau_2016.root
cp ${outdir}/LFVHistos_ZMuTau_2016.root trees/LFVAnalysis_ZMuTau_2016.root
cp ${outdir}/LFVHistos_HEMu_2016.root trees/LFVAnalysis_HEMu_2016.root
cp ${outdir}/LFVHistos_HETau_2016.root trees/LFVAnalysis_HETau_2016.root
cp ${outdir}/LFVHistos_HMuTau_2016.root trees/LFVAnalysis_HMuTau_2016.root

# #Merge samples
hadd ${outdir}/LFVHistos_STtW_2016.root ${outdir}/LFVHistos_Single*ToptW_2016.root
rm ${outdir}/LFVHistos_Single*ToptW_2016.root

hadd histos/latest_production/LFVHistos_QCD_2016.root histos/latest_production/LFVHistos_QCDDoubleEM*_2016.root
rm histos/latest_production/LFVHistos_QCDDoubleEM*_2016.root

#Now do the data

python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/dataprocess/LFVAnalysis_SingleMu_2016.root ${outdir}/LFVHistos_SingleMu_2016.root ${channel}
python generate_histos.py 0 ${doFullSel} rootfiles/latest_production/dataprocess/LFVAnalysis_SingleEle_2016.root ${outdir}/LFVHistos_SingleEle_2016.root ${channel}

hadd ${outdir}/LFVHistos_Data_2016.root ${outdir}/LFVHistos_Single*_2016.root
rm ${outdir}/LFVHistos_SingleMu_2016.root ${outdir}/LFVHistos_SingleEle_2016.root

cp ${outdir}/LFVHistos_Data_2016.root trees/LFVHistos_Data_2016.root
