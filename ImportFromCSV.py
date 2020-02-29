__author__ = "Dzmitry Kudrashou"
__copyright__ = "Copyright 2020, Dzmitry Kudrashou"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

import os
import sys
import csv
import Fusion360Parameters
import importlib
importlib.reload(Fusion360Parameters)

class CSVHelper:
    def __init__(self):
        self.currentFolder = os.path.dirname(__file__)
        self.resourcesPath = os.path.join(self.currentFolder, 'resources/')
        print(self.resourcesPath)
        self.fileNameByKey = {
            "M3": "M3.csv",
            "M4": "M4.csv",
            "M5": "M5.csv"
        }

    def __checkResourcesFolder(self, path):
        print("Check resources folder: " + path)
        if os.path.exists(path):
            print(path + " exists")
            return True
        else:
            print("Error: resources path doesn't exist. \n" + path)
            sys.exit("Exit")
            return False

    def __checkFilePath(self, path):
        if os.path.isfile(path):
            print(path + " exists")
            return True
        else:
            sys.exit("Error: file doesn't exis or it's not a file \n" + path)
            return False

    def importFromRecousrces(self, key):
        fileName = self.fileNameByKey[key]
        filePath = os.path.join(self.resourcesPath, fileName)

        if self.__checkResourcesFolder(self.resourcesPath) == False:
            return False
        if self.__checkFilePath(filePath) == False:
            return True
        if self.checkCSVFile(filePath) == False:
            return True

    def checkCSVFile(self, filePath):
        # ['Name;Value;Units;Comments']
        print("Start to read CSV, " + filePath)
        csvKeysToCheck=['Name', 'Value', 'Units', 'Comments']
        file = open(filePath, 'r')
        csv_Dictionary = csv.DictReader(file)
        headers = csv_Dictionary.fieldnames
        if headers != csvKeysToCheck:
            print("Error: - csv file doesn't contain all necessary keys")
            original = ', '.join([str("'"+elem+"'") for elem in csvKeysToCheck])
            current = ', '.join([str("'"+elem+"'") for elem in headers])
            print("\t original:\t" + original)
            print("\t current:\t" + current)
            sys.exit("Exit")
            return False
        print("Start to update Fusion360 user parameters")
        fusionParameters = Fusion360Parameters.UserParameters()
        for row in csv_Dictionary:
            csvRow = dict(row)
            name = csvRow["Name"]
            value = csvRow["Value"]
            units = csvRow["Units"]
            comments = csvRow["Comments"]
            fusionParameters.updateFusionUserParameters(name, value, units, comments)
    
# CSVHelper().importFromRecousrces("M3")
