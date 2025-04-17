from dataclasses import dataclass
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser

'''
    This Command will view all Airlines

    Can be filtered by:
    - includeDeleted
'''
@dataclass
class ViewAirlinesCommand(CommandHandler):
    includeDeleted : bool = False

    def Validate(self):
        pass

    def Handle(self):
        airlines  = Airline.QueryAll()
        if not self.includeDeleted:
            airlines.data = [d for d in airlines.data if d.DeletedDate == None]
        print(airlines)


class ViewAirlinesCommandParser(CommandParser):

    def __init__(self):
        super().__init__(ViewAirlinesCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-d","-del","-incDel","--includeDeleted", action='store_true', help="If included will also show deleted Airlines")
        parser.set_defaults(command=self.run)