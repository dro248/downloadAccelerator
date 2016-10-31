#! /usr/bin/env python2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--threads', type=int, action='store', help='Specify the number of downloader threads used',default=1)
# parser.add_argument('-u', '--url', type=str, action='store', help='Specify the URL')
parser.add_argument("url")
# parser.add_argument("echo")
args = parser.parse_args()
# print args.url


url = args.url

def check_positive(value):
    if value <=0:
        print "%s is an invalid positive int value" % value
        exit()
    return value
threads = check_positive(args.threads)

print "url:",url
print "threads:",threads
