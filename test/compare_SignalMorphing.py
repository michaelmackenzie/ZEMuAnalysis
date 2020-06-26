import ROOT

#Suppress the opening of many Canvas's
ROOT.gROOT.SetBatch(True) 

#Get all the inputs
fMuMu = ROOT.TFile("workspaces/fit_Mll_SameSign_Muon_Combined.root")
ws_mumu = fMuMu.Get("ws")

fElEl = ROOT.TFile("workspaces/fit_Mll_SameSign_Electron_Combined.root")
ws_elel = fElEl.Get("ws")


fSignal = ROOT.TFile("trees/ZEMuAnalysis_Signal_2016.root")
signal_tree = fSignal.Get("signaltree")

M_ll = ROOT.RooRealVar("M_ll","M_ll",75.,110.)
dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(M_ll),ROOT.RooFit.Import(signal_tree))

pdf_mumu = ws_mumu.pdf("sigpdf")
pdf_ee = ws_elel.pdf("sigpdf")

binned_mumu = pdf_mumu.generateBinned(ROOT.RooArgSet(M_ll),100000000)
binned_elel = pdf_ee.generateBinned(ROOT.RooArgSet(M_ll),100000000)

pdf_mumu_binned = ROOT.RooHistPdf("pdf_mumu_binned","pdf_mumu_binned",ROOT.RooArgSet(M_ll),binned_mumu)
pdf_elel_binned = ROOT.RooHistPdf("pdf_elel_binned","pdf_elel_binned",ROOT.RooArgSet(M_ll),binned_elel)

alpha = ROOT.RooRealVar("alpha","alpha",0.5)

morph_pdf = ROOT.RooIntegralMorph("morph_pdf","morph_pdf",pdf_mumu_binned,pdf_elel_binned,M_ll,alpha)

binned_morphed = morph_pdf.generateBinned(ROOT.RooArgSet(M_ll),1000000000)

morph_pdf_binned = ROOT.RooHistPdf("morph_pdf_binned","morph_pdf_binned",ROOT.RooArgSet(M_ll),binned_morphed,4)

xframe = M_ll.frame(80)
dataset.plotOn(xframe)
morph_pdf_binned.plotOn(xframe)
pdf_mumu_binned.plotOn(xframe,ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed))
pdf_elel_binned.plotOn(xframe,ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kGreen))

c1 = ROOT.TCanvas()
xframe.Draw()
c1.SaveAs("plots/latest_production/2016_2017_2018/compare_morphed_pdf.pdf")

fOut = ROOT.TFile("workspaces/morphed_signal_Combined.root","RECREATE")
fOut.cd()

ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(morph_pdf_binned)

ws.Write()
fOut.Close()

del ws
