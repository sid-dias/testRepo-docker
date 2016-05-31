import glob
import json
import re
import requests
import os


def get_artifact(repo, projName, build_no, fileName):
    username = 'admin'
    password = 'benedict'
    url = 'http://localhost:8081/artifactory/%s/%s/%s/%s' % (repo, projName, build_no, fileName)
    r = requests.get(url, auth=(username, password))
    if not os.path.exists(""+projName):
        os.makedirs(""+projName)
    file = open("%s/%s" % (projName, fileName), "wb")
    file.write(r.content)

for fileName in glob.glob("./build-info/*.json"):
    fd = open(fileName)
    jdata = json.load(fd)

    projName = re.search(r'/([a-zA-Z]+)_', fileName).group(1)
    print(projName)
    repo = jdata["buildInfo"]["properties"]["buildInfo.env.REPOSITORY"]
    build_no = jdata["buildInfo"]["properties"]["buildInfo.env.BUILD_NUMBER"]
    commit_id = jdata["buildInfo"]["properties"]["buildInfo.env.GIT_COMMIT"]

    for artifact in jdata["buildInfo"]["modules"][0]["artifacts"]:
        get_artifact(repo, projName, build_no, artifact["name"])
