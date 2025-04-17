from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airplane import Airplane

'''
    This command will view all airplanes

    Can be filtered by:
    - includeDeleted
'''
@dataclass
class ViewAirplanesCommand(CommandHandler):
    includeDeleted : bool

    def Validate(self):
        pass
    

    def Handle(self):
        airplanes = Airplane.QueryAll()

        # perform this filter in memory here, sorry I couldnt be bothered to create another bespoke query for this
        if not self.includeDeleted:
            airplanes.data = [d for d in airplanes.data if d.DeletedDate == None]
        print(airplanes)


class ViewAirplanesCommandParser(CommandParser):

    def __init__(self):
        super().__init__(ViewAirplanesCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-d","-del","--includeDeleted", action='store_true', help="If included will also show all deleted Airplanes")
        parser.set_defaults(command=self.run)