#!/usr/bin/env python3

"""
    Python script to collect build-info JSON file related to a build corresponding to a job.
"""

import json
import sys
from credentials import ArtifactUser

# Command line argument is the name of the job
projName = sys.argv[1]
user = ArtifactUser()

data = user.make_request('%s/api/build/%s' % (user.artifactory_url, projName)).json()
maxBuildNo = data['buildsNumbers'][0]['uri'][1:]

for obj in data['buildsNumbers']:
    if int(obj['uri'][1:]) > int(maxBuildNo):
        maxBuildNo = obj['uri'][1:]

data = user.make_request('%s/api/build/%s/%s' % (user.artifactory_url, projName, maxBuildNo)).json()
version_no = data["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"]

json_file = open("%s.json" % version_no, "w")
json.dump(data, json_file)
json_file.close()