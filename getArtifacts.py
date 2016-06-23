#!/usr/bin/env python3

"""
    Python script to collect artifacts from various project's builds
    depending on the contents of the "manifest file" whose version
    is specified as a command line argument.
"""

import os
import sys
from credentials import ArtifactUser


def get_artifact(repo, projName, version_no, fileName):
    url = '%s/%s/%s/%s/%s' % (user.artifactory_url, repo, projName, version_no, fileName)
    response = user.make_request(url)

    bin_file = open("artifacts/%s/%s" % (projName, fileName), "wb")
    bin_file.write(response.content)

# Command line argument is the version of the "manifest" file
version = sys.argv[1]
user = ArtifactUser()

url = '%s/manifest/%s/manifest.txt' % (user.artifactory_url, version)
response = user.make_request(url)
manifest_info = str(response.content, encoding="utf-8").split("\n")

if not os.path.exists("artifacts"):
    os.makedirs("artifacts")

for entry in manifest_info[1:]:
    items = entry.split(" ")
    url = '%s/versionInfo/%s/%s.json' % (user.artifactory_url, items[0], items[2])
    response = user.make_request(url)

    jdata = response.json();
    repo = jdata["buildInfo"]["properties"]["buildInfo.env.REPOSITORY"]

    if not os.path.exists("artifacts/" + items[0]):
        os.makedirs("artifacts/" + items[0])

    for artifact in jdata["buildInfo"]["modules"][0]["artifacts"]:
        get_artifact(repo, items[0], items[2], artifact["name"])

    print("Done fetching artifacts of " + items[0])