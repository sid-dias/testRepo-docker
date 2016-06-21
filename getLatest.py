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


data = get_json('http://localhost:8081/artifactory/api/build/manifestUpdate')
maxBuildNo = data['buildsNumbers'][0]['uri'][1:]

for obj in data['buildsNumbers']:
    if int(obj['uri'][1:]) > int(maxBuildNo):
        maxBuildNo = obj['uri'][1:]

data = get_json('http://localhost:8081/artifactory/api/build/manifestUpdate/%s' % maxBuildNo)
if not os.path.exists("build-info"):
    os.makedirs("build-info")

manifest_version=data["buildInfo"]["properties"]["buildInfo.env.manifest_version"]
for artifact in data["buildInfo"]["modules"][0]["artifacts"]:
    url = 'http://localhost:8081/artifactory/manifest/%s/%s' % (manifest_version, artifact["name"])
    r = requests.get(url, auth=(username, password))
    fd = open("build-info/%s" % artifact["name"], "wb")
    fd.write(r.content)
    fd.close()

if not os.path.exists("artifacts"):
    os.makedirs("artifacts")

for fileName in glob.glob("./build-info/*.json"):
    fd = open(fileName)
    jdata = json.load(fd)
    projName = re.search(r'/([a-zA-Z0-9-]+)_', fileName).group(1)
    repo = jdata["buildInfo"]["properties"]["buildInfo.env.REPOSITORY"]
    version_no = jdata["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"]

    for artifact in jdata["buildInfo"]["modules"][0]["artifacts"]:
        get_artifact(repo, projName, version_no, artifact["name"])

    print("Done fetching artifacts of " + projName)
