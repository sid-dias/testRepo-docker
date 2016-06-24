#!/usr/bin/env python3

"""
    Python script to parse JSON files related to the latest build
    of a job and extract the versions to ".params" file.
    It builds the parameter file for the manifest update job's parameters
"""

from credentials import ArtifactUser 

# Project List file contains names of the projects (one per line)
try:
    with open("projectList.txt") as f:
        projNames = f.readlines()
except IOError:
    print("Project List File is not found!")
    raise

param_file = open(".params", "w")
user = ArtifactUser()                                                                  

try:
    for projName in projNames:
        projName = projName.strip("\n")
        name = projName + "-integration"
        build_data = user.make_request('%s/api/build/%s' % (user.artifactory_url, name)).json()

        maxBuildNo = build_data['buildsNumbers'][0]['uri'][1:]
        for obj in build_data['buildsNumbers']:
            if int(obj['uri'][1:]) > int(maxBuildNo):
                maxBuildNo = obj['uri'][1:]

        build_data = user.make_request('%s/api/build/%s/%s' % (user.artifactory_url, name, maxBuildNo)).json()
        version_no = build_data["buildInfo"]["properties"]["buildInfo.env.VERSION_NUMBER"].strip()
        param_file.write("%s_version=%s\n" % (projName, version_no))
except KeyError:
    print("Invalid JSON file received.")
    raise

param_file.write("deploy_docker=true")
param_file.close()