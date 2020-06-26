import ROOT

#Suppress the opening of many Canvas's
ROOT.gROOT.SetBatch(True) 


fInput = ROOT.TFile("histos/latest_production/ZEMuHistos_Data_SameSign_Electron_2016.root")
histo = fInput.Get("htemp")

#Define the observable
M_ll = ROOT.RooRealVar("M_ll","ee invariant mass",110,75.,110.,"GeV")

data = ROOT.RooDataHist("data","data",ROOT.RooArgList(M_ll),histo)

print "Number of events to fit ", data.numEntries()

mean = ROOT.RooRealVar("mean","mean",91.,85.,95.)
width = ROOT.RooRealVar("width","width",2.5,0.1,5.)
sigma = ROOT.RooRealVar("sigma","sigma",2.,0.1,5.)
alpha = ROOT.RooRealVar("alpha","alpha",1.,0.1,10.)
enne = ROOT.RooRealVar("enne","enne",5.,0.1,20.)

mean2 = ROOT.RooRealVar("mean2","mean2",91.,70.,95.)
sigma2 = ROOT.RooRealVar("sigma2","sigma2",5.,0.1,10.)

sigpdf1 = ROOT.RooCBShape("sigpdf1","sigpdf1",M_ll,mean,sigma,alpha,enne)
sigpdf2 = ROOT.RooGaussian("sigpdf2","sigpdf2",M_ll,mean2,sigma2) #,width)

fracsig = ROOT.RooRealVar("fracsig","fracsig",0.7,0.,1.)

sigpdf = ROOT.RooAddPdf("sigpdf","sigpdf",sigpdf1,sigpdf2,fracsig)

a_bkg = ROOT.RooRealVar("a_bkg","a_bkg",0.1,-10.,10.)
b_bkg = ROOT.RooRealVar("b_bkg","b_bkg",0.1,-10.,10.)
c_bkg = ROOT.RooRealVar("c_bkg","c_bkg",0.,-10.,10.)

bkgpdf = ROOT.RooBernstein("bkgpdf","Background PDF",M_ll,ROOT.RooArgList(a_bkg,b_bkg,c_bkg))

N_sig = ROOT.RooRealVar("N_sig","N_sig",20000000.,10000000.,30000000.)
N_bkg = ROOT.RooRealVar("N_bkg","N_bkg",2000000.,10000.,10000000.)

totpdf = ROOT.RooAddPdf("totpdf","Total PDF",ROOT.RooArgList(sigpdf,bkgpdf),ROOT.RooArgList(N_sig,N_bkg))

totpdf.fitTo(data)

xframe = M_ll.frame()
data.plotOn(xframe)
totpdf.plotOn(xframe)
totpdf.plotOn(xframe,ROOT.RooFit.Components("bkgpdf"),ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed))

c1 = ROOT.TCanvas()
xframe.Draw()
c1.SaveAs("plots/latest_production/2016_2017_2018/fit_mll_SameSign_Electron.pdf")

fOut = ROOT.TFile("workspaces/fit_Mll_SameSign_Electron_Combined.root","RECREATE")
fOut.cd()

ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(sigpdf)

ws.Write()
fOut.Close()

del ws
