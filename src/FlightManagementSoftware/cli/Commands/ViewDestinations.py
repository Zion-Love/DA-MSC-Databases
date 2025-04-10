from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This Command Views all the Destinations

    Can be filtered by:
       - desitinationId : can either be singular or multiple
       - countryCode : the country IsoCode to filter for
       - includeInactive
       -

'''

@dataclass
class ViewDestinationsCommand(CommandHandler):
    desintationId : list[int] | int = None
    countryCode : list[str] | str = None
    includeInactive : bool = False
    includeDeleted : bool = False


    def Validate(self):
        pass
    
    def Handle(self):
        raise NotImplementedError()
    

class ViewDestinationsCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewDestinationsCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument('-d','-dest','--destinationId', nargs='+', type=int,help="The DestinationId(s) to view")
        parser.add_argument('-c','-country','--countryCode', nargs='+', type=str, help="The Countrys to filterfor")
        parser.add_argument('-id', '-del', '--includeDeleted', action='store_true', help="If Included will also show the deleted Destinations")
        parser.add_argument('-a','-act','--includeInactive', action='store_true', help="If Included will also show the inactive Destinations")
        parser.set_defaults(command=self.run)