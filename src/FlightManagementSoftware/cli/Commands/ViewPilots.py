
from argparse import ArgumentParser
from dataclasses import dataclass
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.repositories.PilotRepository import pilotRepository

'''
    This Command is used to fetch and view pilots

    Can be filtered by:

'''

@dataclass
class ViewPilotsCommand(CommandHandler):
    SearchName: str = None
    IncludeDeleted: bool = True
    PilotId : int | list[int] = None # TODO implement this filter

    def __post_init__(self):
        self.Validate()
        self.Handle()


    def Validate(self):
        if(self.PilotId):
            assert(self.SearchName == None) , "Cannot provide a SearchName when searching by Id(s)"
            assert(self.IncludeDeleted == None), "Cannot Filter based on Deleted when searching by Id(s)"

        assert(isinstance(self.IncludeDeleted,bool))
        assert(self.SearchName == None or isinstance(self.SearchName,str))
    

    def Handle(self):
        pilots : DataFrame

        if self.PilotId:
            pilots = pilotRepository.QueryById(self.PilotId)

        pilots = pilotRepository.QueryPilots(self.IncludeDeleted, self.SearchName)    
        print(pilots)
        

class ViewPilotsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewPilotsCommand)


    def BuildCommandArgs(self, parser : ArgumentParser) -> ArgumentParser:
        parser.add_argument('--IncludeDeleted', type=bool, help='Toggles weather to show deleted pilots or not', dest='IncludeDeleted')
        parser.add_argument('--SearchName', type=str, help='Filters results fuzzy matching on name', dest='SearchName')
        parser.add_argument('--PilotId', nargs='+', type=int, help="Pilot Id's to search for")

