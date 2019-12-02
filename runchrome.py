#!/usr/bin/python3 
import sys, os
import subprocess, shlex

 #run chrome
def run(quic):
    chrome_cmd = r'sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --headless --enable-benchmarking --enable-net-benchmarking'
    quic_enable = r'--enable-quic'
    if quic == '1':
        command  = chrome_cmd + ' ' + quic_enable;
    else:
        command = chrome_cmd
    print(command)
    subprocess.call(shlex.split(command))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: runchome.py /0")
        print("       1- Quic/HTTP3, 0- HTTP2")
        exit(0);

    run(sys.argv[1]);