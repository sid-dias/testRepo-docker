import sys
import requests
import re
import os

username = 'admin'
password = 'benedict'


version = sys.argv[1]
url = 'http://localhost:8081/artifactory/manifest/%s/' % version
r = requests.get(url, auth=(username, password))

listFile = str(r.content, encoding="utf-8")
fileNames = re.findall(r'\n<a href=\"([^"]*)\"', listFile)
fileNames = list(filter(lambda x: not (x.endswith("md5") or x.endswith("sha1")), fileNames))

if not os.path.exists("build-info"):
    os.makedirs("build-info")

for file in fileNames:
    url = 'http://localhost:8081/artifactory/manifest/%s/%s' % (version, file)
    r = requests.get(url, auth=(username, password))
    fd = open("build-info/%s" % file, "wb")
    fd.write(r.content)
    fd.close()