import ROOT
import copy
import sys

#Supress the opening of many Canvas's
ROOT.gROOT.SetBatch(True)   

runningEra = int(sys.argv[1])
signal_magnify = int(sys.argv[2])

list_inputfiles = []
for filename in sys.argv[3:]:
    list_inputfiles.append(filename)

if runningEra == 0:
    output_dir = "plots/latest_production/2016/"
elif runningEra == 1:
    output_dir = "plots/latest_production/2017/"
elif runningEra == 2:
    output_dir = "plots/latest_production/2018/"
elif runningEra == 3:
    output_dir = "plots/latest_production/2016_2017_2018/"

hstack  = dict()
hsignal = dict()
hdata   = dict()
canvas  = dict()
histo_container = [] #just for memory management

list_histos = ["h_Mmumu", "h_Mee","h_Mmue", "h_lep1pt",
               "h_lep2pt", "h_lep1eta", "h_lep2eta", "h_lep1phi",
               "h_lep2phi", "h_njets25", "h_met_sumEt",
               "h_met_pt", "h_jetptmax", "h_npvs", "h_nbjets25",
               "h_btagid", "h_njets25dr", "h_jetlep1dr", "h_jetlep2dr",
               "h_leppt", "h_lepptoverm", "h_lep1weight", "h_lep2weight",
               "h_cuts"]

for hname in list_histos:
    hstack[hname] = ROOT.THStack("hstack_" + hname,"")

# Color mask must have the same number of entries as non-QCD backgrounds + 1 (that is the cumulative QCD background)
colors_mask = dict()
colors_mask["ttbarWlnu"]           = 12
colors_mask["ttbar"]               = ROOT.kYellow-8
colors_mask["ttbarlnu"]            = ROOT.kAzure+7
colors_mask["DY"]                  = ROOT.kViolet-6
colors_mask["STtW"]                = ROOT.kMagenta+1
colors_mask["WZ"]                  = ROOT.kBlue-7
colors_mask["WW"]                  = ROOT.kPink+1
colors_mask["Wlnu"]                = ROOT.kCyan-7
colors_mask["GammaJets"]           = ROOT.kCyan-1
colors_mask["ZZ"]                  = ROOT.kOrange-3
colors_mask["QCD"]                 = 12

# leg1 = ROOT.TLegend(0.15,0.6120093,0.34,0.9491917) #left positioning
leg1 = ROOT.TLegend(0.6868687,0.6120093,0.9511784,0.9491917) #right positioning
leg1.SetHeader(" ")
leg1.SetFillColor(0)
leg1.SetBorderSize(0)
leg1.SetLineColor(1)
leg1.SetLineStyle(1)
leg1.SetLineWidth(1)
leg1.SetFillStyle(1001)

for filename in list_inputfiles:
    fileIn = ROOT.TFile(filename)

    sample_name = filename.split("_")[2]
    for histo_name in list_histos:
        histo = fileIn.Get(histo_name)
        
        if histo_name == "h_Mmue" :
            histo.Rebin(2)

        # Set to 0 the bins containing negative values, due to negative weights
        hsize = histo.GetSize() - 2 # GetSize() returns the number of bins +2 (that is + overflow + underflow) 
        for bin in range(1,hsize+1): # The +1 is in order to get the last bin
            bincontent = histo.GetBinContent(bin)
            if bincontent < 0.:
                histo.SetBinContent(bin,0.)

        histo_container.append(copy.copy(histo))

        if "Signal" in sample_name:
            histo_container[-1].SetLineStyle(2)   #dashed
            histo_container[-1].SetLineColor(2)   #red
            histo_container[-1].SetLineWidth(4)   #kind of thick
            hsignal[histo_name] = histo_container[-1]
        elif "Data" in sample_name:
            histo_container[-1].SetMarkerStyle(20)   #point
            hdata[histo_name] = histo_container[-1]
        else:
            histo_container[-1].SetFillColor(colors_mask[sample_name])
            hstack[histo_name].Add(histo_container[-1])

        if histo_name == "h_Mmue": #Add the legend only once

            if histo.Integral() > float(signal_magnify)/12. or sample_name == "Signal": #Only plot in the legend those samples which have some contribution
                if not sample_name == "Data" and not sample_name == "Signal":
                    leg1.AddEntry(histo_container[-1],sample_name,"f")
                elif sample_name == "Data":
                    leg1.AddEntry(histo_container[-1],sample_name,"lep")
                elif sample_name == "Signal":
                    leg1.AddEntry(histo_container[-1],sample_name + " x " + str(signal_magnify),"f")

    fileIn.Close()

for histo_name in list_histos:

    canvas[histo_name] = ROOT.TCanvas("Cavas_" + histo_name,"",200,106,600,600)
    canvas[histo_name].cd()

    ##########################################
    pad1 = ROOT.TPad("pad_" + histo_name,"",0,0.28,1,1)
    pad2 = ROOT.TPad("pad_" + histo_name,'',0,0,1,0.25)
    #pad1.SetBottomMargin(0.02)
    #pad1.SetBorderMode(0)
    #pad2.SetTopMargin(0.01)
    #pad2.SetBottomMargin(0.3)
    #pad2.SetBorderMode(0)
    pad1.Draw()
    pad2.Draw()
    ##########################################

    ##########################################
    pad1.cd()
    ##########################################

    hstack[histo_name].SetTitle("")
    hstack[histo_name].Draw("histo")

    ##########################################
    #hstack[histo_name].GetXaxis().SetTickLength(0)
    #hstack[histo_name].GetXaxis().SetLabelOffset(999)
    ##########################################

    if histo_name == "h_Mmumu" :
        hstack[histo_name].GetXaxis().SetTitle("m_{#mu#mu} (GeV)")

    if histo_name == "h_Mee":
        hstack[histo_name].GetXaxis().SetTitle("m_{ee} (GeV)")

    if histo_name == "h_Mmue":
        hstack[histo_name].GetXaxis().SetTitle("m_{#mu e} (GeV)")
    
    if histo_name == "h_leppt":
        hstack[histo_name].GetXaxis().SetTitle("p_{T,ll} (GeV)")

    if histo_name == "h_lepptoverm":
        hstack[histo_name].GetXaxis().SetTitle("p_{T,ll}/M_{ll}")
        
    if histo_name == "h_lep1pt":
        hstack[histo_name].GetXaxis().SetTitle("p_{T,l1} (GeV)")

    if histo_name == "h_lep2pt":
        hstack[histo_name].GetXaxis().SetTitle("p_{T,l2} (GeV)")

    if histo_name == "h_lep1eta":
        hstack[histo_name].GetXaxis().SetTitle("#eta_{l1}")
        hstack[histo_name].SetMaximum(1500.)

    if histo_name == "h_lep2eta":
        hstack[histo_name].GetXaxis().SetTitle("#eta_{l2}")
        hstack[histo_name].SetMaximum(1500.)

    if histo_name == "h_lep1phi":
        hstack[histo_name].GetXaxis().SetTitle("#phi_{l1}")

    if histo_name == "h_lep2phi":
        hstack[histo_name].GetXaxis().SetTitle("#phi_{l2}")

    if histo_name == "h_njets25":
        hstack[histo_name].GetXaxis().SetTitle("Number of jets (p_{T} > 25 GeV/c)")

    if histo_name == "h_nbjets25":
        hstack[histo_name].GetXaxis().SetTitle("Number of b-jets (p_{T} > 25 GeV/c)")

    if histo_name == "h_met_sumEt":
        hstack[histo_name].GetXaxis().SetTitle("#Sigma(E_{T}) (GeV)")

    if histo_name == "h_met_pt":
        hstack[histo_name].GetXaxis().SetTitle("MET p_{T} (25 GeV/c)")
        hstack[histo_name].SetMaximum(1300.)

    if histo_name == "h_jetptmax":
        hstack[histo_name].GetXaxis().SetTitle("p_{T} of hardest jet (25 GeV/c)")

    if signal_magnify != 1:
        hsignal[histo_name].Scale(signal_magnify)      

    hstack[histo_name].Draw("histo")
    hsignal[histo_name].Draw("SAME,hist")
    hdata[histo_name].Draw("SAME,E1")

    hMCErr = copy.deepcopy(hstack[histo_name].GetStack().Last())
    hMCErr.SetFillStyle(3005)
    hMCErr.SetMarkerStyle(1)
    hMCErr.SetFillColor(ROOT.kBlack)
    hMCErr.Draw("sameE2")

    leg1.Draw()

    ################################################
    pad2.cd()
    #pad2.SetTopMargin(0)
    #pad2.SetFillColor(0)
    #pad2.SetFillStyle(0)
    ROOT.gStyle.SetOptStat(0)
    totalMC = copy.deepcopy(hstack[histo_name].GetStack().Last())
    totalData = copy.deepcopy(hdata[histo_name])
    totalData.Divide(totalMC)
    totalData.SetTitle("")
    totalData.SetMarkerStyle(8)
    totalData.SetMarkerColor(1)
    totalData.SetLineColor(1)
    totalData.GetYaxis().SetLabelSize(0.10)
    totalData.GetYaxis().SetTitle("Data/MC")
    totalData.GetYaxis().SetTitleSize(0.08)
    totalData.GetYaxis().SetTitleOffset(0.5)
    # #totalData.GetYaxis().SetRangeUser(0.4,1.6)

    # totalData.GetXaxis().SetLabelSize(0.10)
    # totalData.GetXaxis().SetTitleSize(0.12)
    # totalData.GetXaxis().SetTitleOffset(1.0)

    line_on_one = ROOT.TLine(totalData.GetXaxis().GetXmin(),1.,totalData.GetXaxis().GetXmax(),1.)
    line_on_one.SetLineColor(38)

    totalData.Draw()
    line_on_one.Draw("SAME")
    ################################################

    canvas[histo_name].SaveAs(output_dir + histo_name + ".pdf")
