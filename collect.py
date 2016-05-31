#!/usr/bin/python3

import requests
import json


def get_json(url):
    username = 'admin'
    password = 'benedict'
    r = requests.get(url, auth=(username, password))
    return r.json()

with open("projectList.txt") as f:
    projName = f.readline()
    data = get_json('http://localhost:8081/artifactory/api/build/%s' % projName)

    maxBuildNo = data['buildsNumbers'][0]['uri'][1:]
    for obj in data['buildsNumbers']:
        if obj['uri'][1:] > maxBuildNo:
            maxBuildNo = obj['uri'][1:]

    data = get_json('http://localhost:8081/artifactory/api/build/%s/%s' % (projName, maxBuildNo))
    build_no = data["buildInfo"]["properties"]["buildInfo.env.BUILD_NUMBER"]
    fd = open("%s_%s.json" % (projName, build_no), "w")
    json.dump(data, fd)