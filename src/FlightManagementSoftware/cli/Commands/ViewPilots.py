
from argparse import ArgumentParser
from dataclasses import dataclass
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.repositories.PilotRepository import pilotRepository
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException

'''
    This Command is used to fetch and view pilots

    Can be filtered by:
        - Search Name : fuzzymatches Pilot.Name to this, only accepts single value
        - IncludeDeleted
        - PilotId : either as a single input or list
'''

@dataclass
class ViewPilotsCommand(CommandHandler):
    searchName: str = None
    includeDeleted: bool = True
    pilotId : int | list[int] = None

    def Validate(self):
        if self.pilotId != None:
            if self.searchName != None:
                raise AbortCommandException("Cannot provide a SearchName when searching by Id(s)")

        if self.searchName != None and not isinstance(self.searchName, str):
            raise AbortCommandException(f"Invalid searchName provided : {self.searchName}")
    

    def Handle(self):
        pilots : DataFrame
        if self.pilotId:
            pilots = DataFrame(Pilot.QueryById(self.pilotId), Pilot)
        elif self.searchName != None: 
            pilots = pilotRepository.QueryPilots(self.includeDeleted, self.searchName) 
        else:
            pilots = pilotRepository.QueryPilots(self.includeDeleted, None)

        print(pilots)
        

class ViewPilotsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewPilotsCommand)


    def BuildCommandArgs(self, parser : ArgumentParser) -> ArgumentParser:
        parser.add_argument("-d","-del","--includeDeleted", action='store_true', help='Toggles weather to show deleted pilots or not')
        parser.add_argument("-n","-name","--searchName", type=str, help='Filters results fuzzy matching on name')
        parser.add_argument('-p','--pilotId', nargs='+', type=int, help="Pilot Id's to search for")
        parser.set_defaults(command=self.run)