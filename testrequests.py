import requests

testheader = requests.head("http://cs360.byu.edu", headers={'Accept-Encoding':'identity'})
print "testheader", testheader.headers

header1 = { 'Range':'bytes=0-500', 'Accept-Encoding':'identity'}
header2 = { 'Range':'bytes=501-1094', 'Accept-Encoding':'identity'}

response1 = requests.get("http://cs360.byu.edu", headers=header1)
response2 = requests.get("http://cs360.byu.edu", headers=header2)

print "response1:"
print response1.content
print
print "response2:"
print response2.content
