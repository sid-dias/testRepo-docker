#!/usr/bin/python3
import glob
import json
import re
import requests
import os
import sys

username = 'admin'
password = 'benedict'


def get_artifact(repo, projName, version_no, fileName):
    url = 'http://localhost:8081/artifactory/%s/%s/%s/%s' % (repo, projName, version_no, fileName)
    r = requests.get(url, auth=(username, password))
    if not os.path.exists("artifacts/"+projName):
        os.makedirs("artifacts/"+projName)
    file = open("artifacts/%s/%s" % (projName, fileName), "wb")
    file.write(r.content)

def get_json(url):
    username = 'admin'
    password = 'benedict'
    r = requests.get(url, auth=(username, password))
    return r.json()


with open("projectList.txt") as f:
    projNames = f.readlines()

fd = open(".params", "w")

for projName in projNames:
    projName = projName.strip('\n') + "-integration"
    data = get_json('http://localhost:8081/artifactory/api/build/%s' % projName)
    maxBuildNo = data['buildsNumbers'][0]['uri'][1:]
    for obj in data['buildsNumbers']:
        if obj['uri'][1:] > maxBuildNo:
            maxBuildNo = obj['uri'][1:]

    data = get_json('http://localhost:8081/artifactory/api/build/%s/%s' % (projName, maxBuildNo))
    version_no = data["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"].strip()
    fd.write("%s_version=%s" % (projName, version_no))


fd.close()