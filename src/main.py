from db.sqlite import dbConnectionInstance
from DataTransferObjects.PilotDto import PilotDto
from repositories.PilotRepository import pilotRepository


def __main__():
    dbConnectionInstance.Init_db(refresh=True)
    queryResult = pilotRepository.QueryAll(filterDeleted=False)
    pilotData : PilotDto = PilotDto.Map(queryResult=queryResult)
    print(pilotData)
    input()

if __name__ == "__main__" :
    __main__()