#! /usr/bin/env python2

import requests
import argparse
import sys
import threading

################
# arg checking #
################

usage = "Usage: downloadAccelerator.py [-n threads] url"

# CHECK: number of args
if len(sys.argv) < 3:
    print usage
    exit()

# CHECK: n is a pos int
try:
    numThreads = int(sys.argv[1])
    if numThreads < 1:
	raise Exception()
except Exception:
    print "Arg Error: n must be a positive integer"
    print
    print usage
    exit()

url = sys.argv[2]

# CHECK: url is valid
try:
    r = requests.head(url)
    print r.headers['Accept-Ranges']
    if str(r.status_code)[0] == "4" or str(r.status_code)[0] == "5":
	raise Exception()
except:
    print "Arg Error: Invalid URL provided."
    exit()


#####################################################

########################
# threaded downloading #
########################

for i in range(0, numThreads):
    #spawn downloader thread
    #use timer (for each thread)
        














