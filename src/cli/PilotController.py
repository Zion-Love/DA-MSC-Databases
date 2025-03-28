from repositories.PilotRepository import pilotRepository
from Entities.Pilot import Pilot
from DataFrame import DataFrame
from Entities.EntityMap import entityMap

'''
    This class is used to manipulate entities in the Pilot table

    when loading pilot records from db it will load the into memory so we dont have to refetch them as we are performing
    changes to them
'''

class PilotController:
    def __init__(self):
            self.pilotCollection : DataFrame = None


    def GetPilots(self, showDeleted : bool = False):
        self.pilotCollection = pilotRepository.QueryActivePilots(not showDeleted)


    def AddPilot(self, name : str):
        self.pilotCollection.Append(Pilot(name=name).Create())
        print(self.pilotCollection)


    def DeletePilot(self, Id : int):
        pilot : Pilot = [p for p in self.pilotCollection if p.Id == Id][0]
        self.pilotCollection.remove(pilot)
        pilot.Delete()


    def ViewPilots(self):
         if(self.pilotCollection == None):
              self.GetPilots(False)
         print(self.pilotCollection)
              
         
