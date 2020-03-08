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
        self.fileNameByKey = {
            "M3": "screws/M3.csv",
            "M4": "screws/M4.csv",
            "M5": "screws/M5.csv",
            "B608": "bearings/608.csv",
            "B625": "bearings/625.csv",
            "B626": "bearings/626.csv",
            "B638": "bearings/638.csv",
            "BLinear8": "bearings/linear8.csv",
            "VSlot_2020": "v-slot/VSlot_2020.csv",
            "VProfileNut_M5": "v-slot/VProfileNut_M5.csv",
            "NEMA17_HS2408": "stepper_motor/NEMA17_HS2408.csv",
            "NEMA17_HS4401": "stepper_motor/NEMA17_HS4401.csv",
            "NEMA17_HS8401": "stepper_motor/NEMA17_HS8401.csv",
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

    def printResourcesKeys(self):
        adjustKey = 20
        adjustPath = 30
        print ("Key".ljust(adjustKey), "Path".ljust(adjustPath))
        for key in self.fileNameByKey:
            value = self.fileNameByKey[key]
            print (key.ljust(adjustKey), ("./" + value).ljust(adjustPath))

    def importAll(self):
        for key in self.fileNameByKey:
            self.importFromRecousrces(key)

    def importFromRecousrces(self, key):
        fileName = self.fileNameByKey[key]
        if fileName == None:
            fileName = key + ".csv"
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
        print(str(csv_Dictionary.line_num) + " parameters where updated")
    
# CSVHelper().importFromRecousrces("M3")
try:
    import adsk.core
except ModuleNotFoundError:
    csvHelper = CSVHelper()
    csvHelper.importAll()
    csvHelper.printResourcesKeys()
    pass
