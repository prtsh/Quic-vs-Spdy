#!/usr/bin/python3

import os, sys
import glob
import matplotlib.pyplot as plt 
import subprocess
import statistics


def calculatecdf(plt_http, plt_quic):
    sum_http  = sum(plt_http)
    sum_quic = sum(plt_quic)
    for i in range(1, len(plt_http)):
        plt_http[i] = plt_http[i] + plt_http[i-1]
    for i in range(1, len(plt_quic)):
        plt_quic[i] = plt_quic[i] + plt_quic[i-1] 

    for i in range(0, len(plt_http)):
        plt_http[i] = plt_http[i]/sum_http
    for i in range(0, len(plt_quic)):
        plt_quic[i] = plt_quic[i]/sum_quic

def plotCDF(x1, y1, x2, y2, title):
    plt.plot(x1, y1, color='red', label = 'http2')
    plt.plot(x2, y2, color='green', label = 'quic')  
    plt.xlabel('Page-Load-Time(sec)') 
    plt.ylabel('CDF') 
    plt.title(title) 
    plt.legend() 
    plt.show() 


def parse(bw, loss, rtt, pagetype):
    cwd = os.getcwd();
    harpath = cwd + '/HAR/' 
    os.chdir(harpath)

    #Http2-large-large-bw2-rtt0-loss0-run1-.har
    fileregexQuic = "Quic-{}-bw{}-rtt{}-loss{}-*".format(str(pagetype), str(bw), str(rtt), str(loss));
    fileregexHttp = "Http2-{}-bw{}-rtt{}-loss{}-*".format(str(pagetype), str(bw), str(rtt), str(loss));
    #print(fileregexHttp)
    harfilesHttp = [] 
    for file in glob.glob(fileregexHttp):
        harfilesHttp.append(file)

    harfilesQuic = []
    for file in glob.glob(fileregexQuic):
        harfilesQuic.append(file)

    #print(harfilesHttp, harfilesQuic)
    #os.chdir(cwd)
    plt_quic = []
    plt_http = []
    for harfile in harfilesQuic: 
        #jq -r '.log.pages[] | [.pageTimings.onLoad, .title]|@tsv' baseline.har
        parse_jq = 'jq -r \'.log.pages[] | [.pageTimings.onLoad]|@tsv\' {}'.format(harfile)
        plt = subprocess.check_output(parse_jq, shell=True)
        if (plt.decode('utf-8').strip()) is "":
            continue;
        #print(plt.decode('utf-8').strip())
        plt_quic.append(float(str(plt.decode('utf-8').strip())))
    #print(statistics.mean(plt_quic))
    
    for harfile in harfilesHttp: 
        #jq -r '.log.pages[] | [.pageTimings.onLoad, .title]|@tsv' baseline.har
        parse_jq = 'jq -r \'.log.pages[] | [.pageTimings.onLoad]|@tsv\' {}'.format(harfile)
        plt = subprocess.check_output(parse_jq, shell=True)
        if (plt.decode('utf-8').strip()) is "":
                continue;
        plt_http.append(float(str(plt.decode('utf-8').strip())))
    #print(statistics.mean(plt_http)) 

    plt_http.sort()
    plt_quic.sort()
    plt_http = [x/1000 for x in plt_http] #millisecond to seconds
    plt_quic = [x/1000 for x in plt_quic]
    plt_http_cdf = plt_http[:]
    plt_quic_cdf = plt_quic[:]
    calculatecdf(plt_http_cdf, plt_quic_cdf)
    #print(plt_quic_cdf)
    title = "BW={}, Loss={}, RTT={}, webpage={}".format(bw, loss, rtt, pagetype)
    plotCDF(plt_http, plt_http_cdf,  plt_quic, plt_quic_cdf, title);

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: harparser bandwidth packetlossrate rtt pagetype")
        print(" .     harparser 10 0 200 large-small")
        exit()
    
    #BW=10Mb/s, Loss=0%, RTT=100ms, large-small
    #10 0 200 large-small
    parse(int(sys.argv[1]), (sys.argv[2]), int(sys.argv[3]), str(sys.argv[4]));


