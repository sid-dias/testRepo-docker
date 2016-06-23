"""
    Python Class to read Artifactory user's credentials into private variables
    from ".config" file and make requests using those credentials.
"""

import requests


class ArtifactUser:

    def __init__(self):
        try:
            conf_file = open(".config")
            self.artifactory_url = conf_file.readline().rstrip().split("=")[1]
            self.__username = conf_file.readline().rstrip().split("=")[1]
            self.__password = conf_file.readline().rstrip().split("=")[1]

        except IOError:
            print("No configuration file found!")
            raise

    def make_request(self, url):
        return requests.get(url, auth=(self.__username, self.__password))