from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.repositories.FlightPathRepository import flightPathRepository

'''
    This command will show all flight paths

    can be filtered by:
    - includeDeleted
    - includeInactive
'''

@dataclass
class ViewFlightPathsCommand(CommandHandler):
    includeDeleted : bool = False
    includeInactive : bool = False


    def Validate(self):
        pass


    def Handle(self):
        flightPaths = flightPathRepository.QueryAll(self.includeDeleted, self.includeInactive)
        print(flightPaths)


class ViewFlightPathsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewFlightPathsCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-d","-del","--includeDeleted", action='store_true', help="If included will also return deleted flight paths")
        parser.add_argument("-a","-act","--includeInactive", action='store_true', help="If included will also return inactive flight paths")
        parser.set_defaults(command=self.run)
