#! /usr/bin/env python2

import requests
import argparse
import sys
import threading

####################
# SharedList Class #
####################
class SharedList:
    """ Shared memory """
    def __init__(self):
        self.list = []
        self.sem = threading.Semaphore()
        self.lock = threading.Lock()

    def add(self, item):
        """ add the item the shared list """
        self.sem.acquire()
        self.list.append(item)
        self.sem.release()

    def writeToFile(self):
        sorted(self.list, key=lambda l:l[1])
        print self.list

####################
# Downloader Class #
####################

class Downloader(threading.Thread):
    """ A thread that downloads a part of a file """
    def __init__(self, startByte, endByte, url, sharedList):
       self.startByte = startByte
       self.endByte = endByte
       self.url = url
       self.sharedList = sharedList
       threading.Thread.__init__(self)

    def run(self):
       rangeBody = 'bytes={self.startByte}-{self.endByte}'.format(**locals())
       response = requests.get(self.url, headers={ 'Range': rangeBody, 'Accept-Encoding': 'identity'})
       if str(response.status_code)[0] == '2':
        self.sharedList.add([response.text, self.startByte])




################
# arg checking #
################

# Important Variables
numThreads = 0
url = ""
contentLength = 0

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
    response = requests.head(url, headers={'Accept-Encoding':'identity'})
    contentLength = int(response.headers['Content-Length'])
    if str(response.status_code)[0] == "4" or str(response.status_code)[0] == "5":
	raise Exception()
except:
    print "Arg Error: Invalid URL provided."
    print
    print usage
    exit()



#####################################################



########################
# threaded downloading #
########################
chunkSize = contentLength / numThreads
startByte = 0
endByte = chunkSize
sl = SharedList()

threads = []

for i in range(0, numThreads):
    d = Downloader(startByte, endByte, url, sl)
    threads.append(d)

    # increment "startByte" and "endByte"
    startByte = endByte + 1

    if (endByte + 2*chunkSize) > contentLength:
        # endbyte increments by whatever is left
        endByte += contentLength - endByte
    else:
        endByte += chunkSize

for t in threads:
    t.start()

for t in threads:
    t.join()

#
sl.writeToFile()
