#!/usr/bin/python3
import glob
import json
import re
import requests
import os
import sys

username = 'admin'
password = 'benedict'

def get_json(url):
    username = 'admin'
    password = 'benedict'
    r = requests.get(url, auth=(username, password))
    return r.json()


with open("projectList.txt") as f:
    projNames = f.readlines()

fd = open(".params", "w")

for projName in projNames:
    projName = projName.strip("\n")
    name = projName + "-integration"
    data = get_json('http://localhost:8081/artifactory/api/build/%s' % name)
    maxBuildNo = data['buildsNumbers'][0]['uri'][1:]
    for obj in data['buildsNumbers']:
        if obj['uri'][1:] > maxBuildNo:
            maxBuildNo = obj['uri'][1:]

    data = get_json('http://localhost:8081/artifactory/api/build/%s/%s' % (name, maxBuildNo))
    version_no = data["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"].strip()
    fd.write("%s_version=%s\n" % (projName, version_no))

fd.write("deploy_docker=true")
fd.close()
