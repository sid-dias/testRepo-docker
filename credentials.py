
"""
    Python Class to read Artifactory user's credentials into private variables
    from "artifactory_credentials" file and make requests using those credentials.
"""

import requests


class ArtifactUser:

    def __init__(self):
        try:
            cred_file = open("artifactory_credentials")
            self.artifactory_url = cred_file.readline().rstrip().split("=")[1]
            self.__username = cred_file.readline().rstrip().split("=")[1]
            self.__password = cred_file.readline().rstrip().split("=")[1]
        except IOError:
            print("No configuration file found!")
            raise

    def make_request(self, url):
        return requests.get(url, auth=(self.__username, self.__password))
