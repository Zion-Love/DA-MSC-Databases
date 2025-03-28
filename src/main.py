from db.sqlite import dbConnectionInstance
from DataTransferObjects.PilotDto import PilotDto
from repositories.PilotRepository import pilotRepository
from Entities.EntityMap import entityMap
from Entities.Pilot import Pilot
from DataFrame import DataFrame

def __main__():
    dbConnectionInstance.Init_db(refresh=True)
    pilots = Pilot.QueryAll()
    print(pilots)
    pilots[1].Delete()
    pilots = Pilot.QueryAll()
    print(pilots)
    input()

if __name__ == "__main__" :
    __main__()