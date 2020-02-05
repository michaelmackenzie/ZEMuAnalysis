import ROOT
import argparse

#---------------------------------#
p = argparse.ArgumentParser(description='Select the year')
p.add_argument('year_option', help='Type <<2016>>, <<2017>> or <<2018>>')
args = p.parse_args()

year = args.year_option

fMuonIn = ROOT.TFile("rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleMu_" + year + ".root")
muon_tree = fMuonIn.Get("Events")

muon_tree.Draw("M_ll","nMuon==2")

histo_mu = muon_tree.GetHistogram()

fOut = ROOT.TFile("histos/latest_production/ZEMuHistos_Data_SameSign_Muon_" + year ".root","RECREATE")
fOut.cd()
histo_mu.Write()
fOut.Close()

fEleIn = ROOT.TFile("rootfiles/latest_production/dataprocess/ZEMuAnalysis_SingleEle_" + year + ".root")
ele_tree = fEleIn.Get("Events")

ele_tree.Draw("M_ll","nElectron==2")

histo_ele = ele_tree.GetHistogram()

#need to reopen to avoid memory leaks
fOut = ROOT.TFile("histos/latest_production/ZEMuHistos_Data_SameSign_Electron_" + year + ".root","RECREATE")
fOut.cd()
histo_ele.Write()
fOut.Close()
