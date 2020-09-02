###All normalizations are provided to 1fb-1 of lumi in these tables
import os
import sys
import argparse

#---------------------------------#
p = argparse.ArgumentParser(description='Select the year')
p.add_argument('year_option', help='Type <<2016>>, <<2017>> or <<2018>>')
args = p.parse_args()

year = args.year_option
#---------------------------------#

#xsec lookup in pb
secs_table = dict()
secs_table["ttbarToSemiLeptonic"] = 365.34 # accounting for the 2 possible charge signs of the W
secs_table["ttbarlnu"] = 88.29 #NNLO-2018
secs_table["QCDPt30toInf"] = 242700.0
secs_table["QCDPt40toInf"] = 117400.0
secs_table["SingleToptW"] = 34.91
secs_table["SingleAntiToptW"] = 34.97
secs_table["DY50"] = 2075.14*3 #amcatnlo 2017
secs_table["WW"] = 12.178
secs_table["WZ"] = 27.6
secs_table["Wlnu"] = 52850.0
secs_table["ZEMu"] = 2075.14*0.000001/0.0337 #Assume BR of 10-6
secs_table["ZETau"] = ((6225.42+18610.)/(3.*3.3658e-2))*9.8e-6
secs_table["ZMuTau"] = ((6225.42+18610.)/(3.*3.3658e-2))*1.2e-5
secs_table["HEMu"] = (48.61+3.766+0.5071+1.358+0.880)*3.5e-4
secs_table["HETau"] = (48.61+3.766+0.5071+1.358+0.880)*6.1e-3
secs_table["HMuTau"] = (48.61+3.766+0.5071+1.358+0.880)*2.5e-3

#######################################
#                                     #
#--------------- 2016 ----------------#
#                                     #
#######################################
#fraction of negative-weighted events in NLO samples (2016)
frac_table_2016 = dict()
frac_table_2016["ttbarToSemiLeptonic"] = 0.
frac_table_2016["ttbarlnu"] = 0.
frac_table_2016["SingleToptW"] = 0.003708
frac_table_2016["SingleAntiToptW"] = 0.00369
frac_table_2016["DY50"] = 0.1661
frac_table_2016["WW"] = 0.1866
frac_table_2016["WZ"] = 0.
frac_table_2016["Wlnu"] = 0.
frac_table_2016["ZEMu"] = 0.
frac_table_2016["ZETau"] = 0.
frac_table_2016["ZMuTau"] = 0.
frac_table_2016["HEMu"] = 0.
frac_table_2016["HETau"] = 0.
frac_table_2016["HMuTau"] = 0.

#######################################
#                                     #
#--------------- 2017 ----------------#
#                                     #
#######################################
#fraction of negative-weighted events in NLO samples (2017)
frac_table_2017 = dict()
frac_table_2017["ttbarToSemiLeptonic"] = 0.
frac_table_2017["ttbarlnu"] = 0.
frac_table_2017["SingleToptW"] = 0.003758
frac_table_2017["SingleAntiToptW"] = 0.0034
frac_table_2017["DY50"] = 0.1624
frac_table_2017["WW"] = 0.
frac_table_2017["WZ"] = 0.
frac_table_2017["Wlnu"] = 0.
frac_table_2017["ZEMu"] = 0.
frac_table_2017["ZETau"] = 0.
frac_table_2017["ZMuTau"] = 0.
frac_table_2017["HEMu"] = 0.
frac_table_2017["HETau"] = 0.
frac_table_2017["HMuTau"] = 0.

#######################################
#                                     #
#--------------- 2018 ----------------#
#                                     #
#######################################
#fraction of negative-weighted events in NLO samples (2018)
frac_table_2018 = dict()
frac_table_2018["ttbarToSemiLeptonic"] = 0.
frac_table_2018["ttbarlnu"] = 0.
frac_table_2018["QCDPt30toInf"] = 0.
frac_table_2018["QCDPt40toInf"] = 0.
frac_table_2018["SingleToptW"] = 0.003758
frac_table_2018["SingleAntiToptW"] = 0.0034
frac_table_2018["DY50"] = 0.163
frac_table_2018["WW"] = 0.001755
frac_table_2018["WZ"] = 0.
frac_table_2018["Wlnu"] = 0.0003866
frac_table_2018["ZEMu"] = 0.
frac_table_2018["ZETau"] = 0.
frac_table_2018["ZMuTau"] = 0.
frac_table_2018["HEMu"] = 0.
frac_table_2018["HETau"] = 0.
frac_table_2018["HMuTau"] = 0.

frac_table = dict()

complementary_samples_list_2016 = []
complementary_samples_list_2017 = []
complementary_samples_list_2018 = []

if year == "2016":
    complementary_samples_list = complementary_samples_list_2016
    frac_table = frac_table_2016

if year == "2017":
    complementary_samples_list = complementary_samples_list_2017
    frac_table = frac_table_2017

if year == "2018":
    complementary_samples_list = complementary_samples_list_2018
    frac_table = frac_table_2018

##Now starts the program
def main():

    dir_input = "crab_projects/samples_MC_" + year + "/"
    list_dirs = os.listdir(dir_input)

    if not os.path.exists("rootfiles"):
        os.makedirs("rootfiles")
    if not os.path.exists("rootfiles/latest_production"):
        os.makedirs("rootfiles/latest_production")
    if not os.path.exists("rootfiles/latest_production/MC"):
        os.makedirs("rootfiles/latest_production/MC")
    if not os.path.exists("rootfiles/latest_production/MC/normalizations"):
        os.makedirs("rootfiles/latest_production/MC/normalizations")

    output_filename = "rootfiles/latest_production/MC/normalizations/Normalizations_table_" + year + ".txt" 
    out_file = open(output_filename,"w")

    events_cumul = dict()
    for sample in complementary_samples_list:
        events_cumul[sample] = 0.

    for dirname in list_dirs:

        is_in_complementary_sample_list = False
        
        samplename = dirname.split("crab_" + year + "_LFVAnalysis_")[1]

        print "Processing sample dir " + dirname
        crab_command = "crab report -d " + dir_input + dirname + " | grep read | awk '{print $5}'"
        #print crab_command

        event_string = os.popen(crab_command).read()
        number_events = float(event_string)
        print "No. of events processed = " + event_string + "\n"
        
        #Treat differently different samples with same xsec
        for name_complement in complementary_samples_list:
            if name_complement in samplename:
                events_cumul[name_complement] = events_cumul[name_complement] + number_events*(1-2*frac_table[name_complement])
                print "events_cumul: ", events_cumul[name_complement]
                is_in_complementary_sample_list = True
                continue
        if not is_in_complementary_sample_list:
            events_cumul[samplename] = number_events*(1-2*frac_table[samplename])

    for sample,event_count in events_cumul.iteritems():
        if event_count == 0:
            scale_factor = 0.
            print "NUMBER OF EVENTS RETRIEVED = 0. SCALE FACTOR SET TO 0"
        else:
            xsection = secs_table[sample]
            print "Cross section = ", xsection
            scale_factor = float(xsection*1000./events_cumul[sample])
            print sample + " scale factor = ", scale_factor

        write_string = sample + " " + str(scale_factor) + "\n"
        print "Output Norm = ", write_string
        out_file.write(write_string)        
            
    print "All done!"

if __name__ == "__main__":
    main()
