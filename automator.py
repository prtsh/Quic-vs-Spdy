#!/usr/bin/python3
# if you are runngn this on mac, make sure that the sudo - password prompt is not required
# sudo visudo, then, add the line: %admin ALL=(ALL) NOPASSWD: ALL
import sys, os
import subprocess
import json
import time
import shlex
import shutil

def run(isQuick):
    reset_dnctl = r'sudo dnctl -q flush'
    reset_pfctl = r'sudo pfctl -f /etc/pf.conf'
    cwd = os.getcwd()

    append = ""
    if isQuick == '1':
        append = 'Quic-'
    else:
        append = 'Http2-'

    urllist = []
    with open(cwd + '/urls.txt', 'r') as url:
        urllist = (url.readlines());
    
    pathHAR = cwd + '/HAR/'
    #delete the current HAR files and create new files
    if os.path.isdir(pathHAR) != True:
        #shutil.rmtree(pathHAR)
        os.mkdir(pathHAR)
    
    for bw in [2, 10]: #unit Mbps
        for rtt in [0, 100]: #unit ms
            for loss in [0, 0.02]: #unit % in fraction
                for run in range(1,51):
                    command = r'./trafficshaper.sh {b} {d} {p}'.format(b=bw, d=rtt, p=loss) 
                    print(command)
                    subprocess.call(shlex.split(command))
                    time.sleep(2)
                    #run HAR capture and save the HAR file
                    for url in urllist:
                        url = url.strip();
                        harfile = pathHAR + append + url.split('/')[-1].strip();
                        harfile = harfile + '-bw{}-rtt{}-loss{}-run{}-.har' \
                            .format(str(bw), str(rtt), str(loss), str(run));
                        har_cmd = r'chrome-har-capturer -o {} {}'.format(harfile, url)
                        os.system(har_cmd);

    #reset traffic mod before each run
    os.system(reset_dnctl);
    os.system(reset_pfctl);

if __name__ == "__main__":
    #make sure the argument is same as used in
    if len(sys.argv) != 2:
        print("Usage: automator.py 1/0")
        print("       1- Quic/HTTP3, 0- HTTP2")
        exit(0);

    run(sys.argv[1]);
