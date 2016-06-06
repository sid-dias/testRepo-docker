#!/usr/bin/python3

import requests
import json
import sys


def get_json(url):
    username = 'admin'
    password = 'benedict'
    r = requests.get(url, auth=(username, password))
    return r.json()


projName = sys.argv[1]
data = get_json('http://localhost:8081/artifactory/api/build/%s' % projName)
maxBuildNo = data['buildsNumbers'][0]['uri'][1:]

for obj in data['buildsNumbers']:
    print(obj['uri'][1:])
    if int(obj['uri'][1:]) > int(maxBuildNo):
        maxBuildNo = obj['uri'][1:]

data = get_json('http://localhost:8081/artifactory/api/build/%s/%s' % (projName, maxBuildNo))
version_no = data["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"]

fd = open("%s.json" %version_no, "w")
json.dump(data, fd)
fd.close()
