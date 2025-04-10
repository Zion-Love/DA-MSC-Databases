
from argparse import ArgumentParser
from dataclasses import dataclass
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.repositories.PilotRepository import pilotRepository
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException

'''
    This Command is used to fetch and view pilots

    Can be filtered by:
        - Search Name : fuzzymatches Pilot.Name to this
        - IncludeDeleted
        - PilotId
'''

@dataclass
class ViewPilotsCommand(CommandHandler):
    searchName: str = None
    includeDeleted: bool = True
    pilotId : int | list[int] = None

    def Validate(self):
        if self.pilotId:
            if self.searchName == None:
                raise AbortCommandException("Cannot provide a SearchName when searching by Id(s)")

        if not (self.searchName == None or isinstance(self.searchName,str)):
            raise AbortCommandException(f"Invalid searchName provided : {self.searchName}")
    

    def Handle(self):
        pilots : DataFrame
        if self.pilotId:
            pilots = pilotRepository.QueryById(self.pilotId)

        pilots = pilotRepository.QueryPilots(self.includeDeleted, self.searchName)    
        print(pilots)
        

class ViewPilotsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewPilotsCommand)


    def BuildCommandArgs(self, parser : ArgumentParser) -> ArgumentParser:
        parser.add_argument('-includeDeleted', nargs='?',type=bool, help='Toggles weather to show deleted pilots or not', dest='IncludeDeleted')
        parser.add_argument('--searchName', nargs='?',type=str, help='Filters results fuzzy matching on name', dest='SearchName')
        parser.add_argument('--pilotId', nargs='*', type=int, help="Pilot Id's to search for")
        parser.set_defaults(command=self.run)