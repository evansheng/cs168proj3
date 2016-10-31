import numpy as np
import subprocess
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
from matplotlib.backends import backend_pdf
 

def run_ping(hostnames, num_packets, raw_ping_output_filename, aggregated_ping_output_filename):
    rawOutputs = {}
    aggOutputs = {}
    for hostname in hostnames:
        try:
            ls_output = subprocess.check_output("ping " + "-c " + str(num_packets) + " " + hostname , shell=True)
        except subprocess.CalledProcessError as e:
            rawOutputs[hostname] = [-1]*num_packets
            agged = {}
            agged["drop_rate"] = 100
            agged["median_rtt"] = -1
            agged["max_rtt"] = -1
            aggOutputs[hostname] = agged
            continue
        linesplit = ls_output.split("\n")
        rttList = []
        seqnum = 1
        for line in linesplit:
            print line
            if "ms" in line and "bytes" in line and "PING" not in line.split():
                line = line.split()
                while line[len(line) - 4].split("=")[1] != str(seqnum):
                    rttList.append(-1)
                    seqnum += 1
                rttList.append(float(line[len(line) - 2].split("=")[1]))
                seqnum += 1
                
            if not line:
                while seqnum != num_packets+1:
                    rttList.append(-1)
                    seqnum += 1
        rawOutputs[hostname] = rttList
        aggOutputs[hostname] = getAggs(rttList)
    print rawOutputs
    with open(raw_ping_output_filename, 'w') as outfile:
        json.dump(rawOutputs, outfile)
    print aggOutputs
    with open(aggregated_ping_output_filename, 'w') as outfile:
        json.dump(aggOutputs, outfile)
    
def getAggs(rawList):
    aggDict = {}
    count = 0
    for time in rawList:
        if time == -1:
            count += 1
    aggDict["drop_rate"] = count/len(rawList)
    
    filtered = [float(x) for x in rawList if x != -1]
    if not filtered:
        aggDict["median_rtt"] = -1
        aggDict["max_rtt"] = -1
    else:
        aggDict["median_rtt"] = np.median(np.array(filtered))
        aggDict["max_rtt"] = max(filtered)
    return aggDict
    
def plot_median_rtt_cdf(agg_ping_results_filename, output_cdf_filename):
    with open(agg_ping_results_filename) as data_file:    
        data = json.load(data_file)
    medians = []
    for k, v in data.iteritems():
        if v["median_rtt"] != -1:
            medians.append(v["median_rtt"])
    medians.sort()
    cumulative = np.cumsum(medians)
    cumulative /= sum(medians)
    plot.plot(medians, cumulative, label = "MEDIAN RTTs")
    # f, ax = plot.subplots()
    # ax.plot(medians, cumulative)
    # f.savefig("medianplot.pdf")
    plot.legend(loc = "upper left")
    plot.xlabel("RTT's")
    plot.grid()
    
    my_filepath = output_cdf_filename
    with backend_pdf.PdfPages(my_filepath) as pdf:
      pdf.savefig()
      
def plot_ping_cdf(raw_ping_results_filename, output_cdf_filename):
    with open(raw_ping_results_filename) as data_file:
        data = json.load(data_file)
    hostnames = []
    for k,v in data.iteritems():
        hostnames.append(k)
        v.sort()
        cumulative = np.cumsum(v)/s
        plot.plot(v,)
    plot.legend(hostnames)
    my_filepath = output_cdf_filename
    with backend_pdf.PdfPages(my_filepath) as pdf:
      pdf.savefig()

    
if __name__ == "__main__":
    with open("alexa_top_100") as data_file:
        top100 =  [line.strip() for line in data_file.readlines()]
    #run_ping(["google.com", "weibo.com"], 4, "raw_out", "ag_out")
    #plot_median_rtt_cdf("ag_out", "poop")
    
    #experiment a and b
    #run_ping(top100, 10, "rtt_a_raw.json", "rtt_a_agg.json")
    #run_ping(["google.com", "todayhumor.co.kr", "zanvarsity.ac.tz", "taobao.com"], 500, "rtt_b_raw.json", "rtt_b_agg.json")
    #graphs for a and b
    plot_median_rtt_cdf("rtt_a_agg.json", "part1-1.pdf")
    plot_ping_cdf("rtt_b_raw.json", "part1-2.pdf")