import ROOT
import math
import argparse

#Suppress the opening of many Canvas's
ROOT.gROOT.SetBatch(True) 

#Get all the inputs
fBkg = ROOT.TFile("trees/ZEMuAnalysis_Background_2016.root")
signaltree = fBkg.Get("signaltree")

M_ll = ROOT.RooRealVar("M_ll","M_ll",75.,110.,"GeV")
mcweight = ROOT.RooRealVar("mcweight","mcweight",1.,-100.,100.)
dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(M_ll,mcweight),ROOT.RooFit.Import(signaltree),ROOT.RooFit.WeightVar(mcweight))

#fInput_mumu = ROOT.TFile("histos/latest_production/ZEMuHistos_Data_SameSign_Muon_2018.root")
#histo_mu = fInput_mumu.Get("htemp")
#fInput_elel = ROOT.TFile("histos/latest_production/ZEMuHistos_Data_SameSign_Electron_2018.root")
#histo_el = fInput_elel.Get("htemp")

N_mumu = 29409600.
N_ee = 12157600.

print "Number of events in the fit is ", dataset.sumEntries()
print "The number of mumu events is ", N_mumu
print "The number of ee events is ", N_ee

#Get the signal PDF
fWSSignal = ROOT.TFile("workspaces/morphed_signal_Combined.root")
ws_signal = fWSSignal.Get("ws")

sigPDF = ws_signal.pdf("morph_pdf_binned")

#Background PDF
a_bkg = ROOT.RooRealVar("a_bkg","a_bkg",3.28640,-50.,50.)
b_bkg = ROOT.RooRealVar("b_bkg","b_bkg",-0.290163,-50.,50.)
c_bkg = ROOT.RooRealVar("c_bkg","c_bkg",0.558070,-50.,50.)
d_bkg = ROOT.RooRealVar("d_bkg","d_bkg",0.264009,-50.,50.)

bkgPDF = ROOT.RooBernstein("bkgPDF","Background PDF",M_ll,ROOT.RooArgList(a_bkg,b_bkg,c_bkg,d_bkg))

#Compose the total PDF
br_emu = ROOT.RooRealVar("br_emu","br_emu",0.,-0.00001,0.1)
br_ll = ROOT.RooRealVar("br_ll","br_ll",0.033632)

#Add lognormal systematics
# First is direct systematics on N_emu
eff_nominal   = ROOT.RooRealVar("eff_nominal","eff_nominal",1.)
eff_kappa     = ROOT.RooRealVar("eff_kappa","eff_kappa",1.03)
beta_eff      = ROOT.RooRealVar("beta_eff","beta_eff",0.,-5.,5.)
eff           = ROOT.RooFormulaVar("eff","@0 * pow(@1,@2)",ROOT.RooArgList(eff_nominal,eff_kappa,beta_eff))
global_eff    = ROOT.RooRealVar("global_eff","global_eff",0.,-5.,5.)
one           = ROOT.RooRealVar("one","one",1.)
constrain_eff = ROOT.RooGaussian("constrain_eff","constrain_eff",global_eff,beta_eff,one)
global_eff.setConstant(1)

#N_ee and N_mumu systematics
N_mumu_nominal = ROOT.RooRealVar("N_mumu_nominal","N_mumu_nominal",N_mumu)
N_ee_nominal   = ROOT.RooRealVar("N_ee_nominal","N_ee_nominal",N_ee)
N_mumu_kappa   = ROOT.RooRealVar("N_mumu_kappa","N_mumu_kappa",1.+1./math.sqrt(N_mumu))
N_ee_kappa     = ROOT.RooRealVar("N_ee_kappa","N_ee_kappa",1.+1./math.sqrt(N_ee))
beta_N_mumu    = ROOT.RooRealVar("beta_N_mumu","beta_N_mumu",0.,-5.,5.)
beta_N_ee      = ROOT.RooRealVar("beta_N_ee","beta_N_ee",0.,-5.,5.)
N_mumu_var     = ROOT.RooFormulaVar("N_mumu_var","@0 * pow(@1,@2)",ROOT.RooArgList(N_mumu_nominal,N_mumu_kappa,beta_N_mumu))
N_ee_var       = ROOT.RooFormulaVar("N_ee_var","@0 * pow(@1,@2)",ROOT.RooArgList(N_ee_nominal,N_ee_kappa,beta_N_ee))
global_N_mumu  = ROOT.RooRealVar("global_N_mumu","global_N_mumu",0.,-5.,5.)
global_N_ee    = ROOT.RooRealVar("global_N_ee","global_N_ee",0.,-5.,5.)
constr_N_mumu  = ROOT.RooGaussian("constr_N_mumu","constr_N_mumu",global_N_mumu,beta_N_mumu,one)
constr_N_ee    = ROOT.RooGaussian("constr_N_ee","constr_N_ee",global_N_ee,beta_N_ee,one)
global_N_mumu.setConstant(1)
global_N_ee.setConstant(1)

N_sig = ROOT.RooFormulaVar("N_sig","@0*@4*sqrt((@1*@2)/(@3*@3))",ROOT.RooArgList(br_emu,N_ee_var,N_mumu_var,br_ll,eff))
N_bkg = ROOT.RooRealVar("N_bkg","N_bkg",500.,0.,100000.)

totPDF = ROOT.RooAddPdf("totPDF","totPDF",ROOT.RooArgList(sigPDF,bkgPDF),ROOT.RooArgList(N_sig,N_bkg))
totPDF_constr = ROOT.RooProdPdf("totPDF_constr","totPDF_constr",ROOT.RooArgList(totPDF,constrain_eff,constr_N_mumu,constr_N_ee))

#Alternate background function
tau_bkg = ROOT.RooRealVar("tau_bkg","tau_bkg",-0.0583634,-5000.,0.)
bkgPDF_exp = ROOT.RooExponential("bkgPDF_exp","bkgPDF_exp",M_ll,tau_bkg)
totPDF_alt = ROOT.RooAddPdf("totPDF_alt","totPDF_alt",ROOT.RooArgList(sigPDF,bkgPDF_exp),ROOT.RooArgList(N_sig,N_bkg))
totPDF_constr_alt = ROOT.RooProdPdf("totPDF_constr_alt","totPDF_constr_alt",ROOT.RooArgList(totPDF_alt,constrain_eff,constr_N_mumu,constr_N_ee))
totPDF_constr_alt.fitTo(dataset)

#Fit, plot, etc
totPDF_constr.fitTo(dataset,ROOT.RooFit.Extended(1))

xframe = M_ll.frame()
dataset.plotOn(xframe)
totPDF_constr.plotOn(xframe)
bkgPDF_exp.plotOn(xframe,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineStyle(ROOT.kDashed))

c1 = ROOT.TCanvas()
xframe.Draw()
c1.SaveAs("plots/latest_production/2016_2017_2018/fit_bkgonly.pdf")

#Save the fit result
fOut = ROOT.TFile("workspaces/fit_Mll_Backgroundonly_Combined.root","RECREATE")
fOut.cd()

bkg_data = bkgPDF.generate(ROOT.RooArgSet(M_ll),N_bkg.getVal())

ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(totPDF_constr)
getattr(ws,'import')(totPDF_constr_alt,ROOT.RooFit.RecycleConflictNodes())
getattr(ws,'import')(bkg_data)

ws.Print()

ws.Write()
fOut.Close()

del ws
