__author__ = "Dzmitry Kudrashou"
__copyright__ = "Copyright 2020, Dzmitry Kudrashou"
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Production"

moduleImported = True
try:
    import adsk.core, adsk.fusion, traceback
except ModuleNotFoundError:
    moduleImported = False
    pass


class UserParameters:

    def __init__(self):
        self.ui = None
        if moduleImported == False:
            print("Error: Module wasn't imported")
            return
        try:
            self.app = adsk.core.Application.get()
            self.ui  = self.app.userInterface
            self.design = self.app.activeProduct
            self.userParams = self.design.userParameters
        except:
            if self.ui:
                self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    def updateFusionUserParameters(self, name, value, units, comments):
        if moduleImported == False:
            print("Error: Modules `adsk.core, adsk.fusion, traceback` wasn't imported")
            return
        if self.userParams.itemByName(name) == None:
            self.__addNewUserParameter(name, value, units, comments)
        else:
            self.__updateUserParameter(name, value, units, comments)
    
    def __addNewUserParameter(self, name, value, units, comments):
        print("Add parameters: Name: " + name + ", Value: " + value + ", Units: " + units + ", Comments: " + comments)
        aUserValue = adsk.core.ValueInput.createByString(value)
        aUnits = self.design.unitsManager.defaultLengthUnits
        self.userParams.add(name, aUserValue, aUnits, comments)
    
    def __updateUserParameter(self, name, value, units, comments):
        print("Update parameters: Name: " + name + ", Value: " + value + ", Units: " + units + ", Comments: " + comments)
        aUserValue = adsk.core.ValueInput.createByString(value)
        aUnits = self.design.unitsManager.defaultLengthUnits
        self.userParams.itemByName(name).expression = value

            
        