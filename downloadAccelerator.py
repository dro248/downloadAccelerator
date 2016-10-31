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

    def writeToFile(self, filename):
        self.list.sort()

        with open(filename, 'wb') as f:
            for item in self.list:
                f.write(item[1])
        # print totalFile


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
        self.sharedList.add([self.startByte, response.content])




################
# arg checking #
################

# NUM_OF_THREADS = 1
# URL = ""
# CONTENT_LENGTH = 0

usage = "Usage: downloadAccelerator.py [-n threads] url"

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--threads', type=int, action='store', help='Specify the number of downloader threads used',default=1)
parser.add_argument("url")
args = parser.parse_args()

# CHECK: url is valid
def validate_url(test_url):
    try:
        response = requests.head(test_url, headers={'Accept-Encoding':'identity'})
        # CONTENT_LENGTH = int(response.headers['Content-Length'])
        if str(response.status_code)[0] == "4" or str(response.status_code)[0] == "5":
            raise Exception()
        return test_url
    except:
        print "Arg Error: Invalid URL provided."
        print
        print usage
        exit()



def check_positive(value):
    if value <=0:
        print "%s is an invalid positive int value" % value
        exit()
    return value


# Important Variables
URL = validate_url(args.url)
NUM_OF_THREADS = check_positive(args.threads)
CONTENT_LENGTH = int(requests.head(URL, headers={'Accept-Encoding':'identity'}).headers['Content-Length'])

print "url:", URL
print "threads:", NUM_OF_THREADS
print "Content-Length", CONTENT_LENGTH




















#get filename given url
def getFilename(url):
    filename = "index.html" if (url.split('/')[-1] == "") else url.split('/')[-1]
    return filename

#####################################################



########################
# threaded downloading #
########################
chunkSize = CONTENT_LENGTH / NUM_OF_THREADS
startByte = 0
endByte = chunkSize
sl = SharedList()

threads = []

for i in range(0, NUM_OF_THREADS):
    d = Downloader(startByte, endByte, URL, sl)
    threads.append(d)

    # increment "startByte" and "endByte"
    startByte = endByte + 1

    if (endByte + 2*chunkSize) > CONTENT_LENGTH:
        # endbyte increments by whatever is left
        endByte += CONTENT_LENGTH - endByte
    else:
        endByte += chunkSize

for t in threads:
    t.start()

for t in threads:
    t.join()

# write SharedList to file
sl.writeToFile(getFilename(URL))
