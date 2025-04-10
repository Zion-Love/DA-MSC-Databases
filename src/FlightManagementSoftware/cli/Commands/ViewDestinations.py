from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This Command Views all the Destinations

    Can be filtered by:
       - showInactive

'''

# TODO :

@dataclass
class ViewDestinationsCommand(CommandHandler):
    desintationId : list[int] | int = None
    countryCodeFilters : list[str] | str = None
    includeDeleted : bool = False


    def Validate(self):
        pass
    
    def Handle(self):
        raise NotImplementedError()
    

class ViewDestinationsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewDestinationsCommand)

    def BuildCommandArgs(self, parser):
        parser.set_defaults(command=self.run)