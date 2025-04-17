# TODO
from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.repositories.AirlineRepository import airlineRepository

@dataclass
class ViewAirlinePilotSummaryCommand(CommandHandler):
    airlineId : list[int] = None
    includeDeleted: bool = False

    def Validate(self):
        pass

    def Handle(self):
        summary = airlineRepository.QuerySummary(airlineId=self.airlineId, includeDeleted=self.includeDeleted)
        print(summary)

class ViewAirlinePilotSummaryCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewAirlinePilotSummaryCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-a","-aId","--airlineId", nargs='+', type=int, help="Airline Ids to filter for")
        parser.add_argument("-id","-incDel","--includeDeleted", action="store_true", help="If included will also show deleted Airlines")
        parser.set_defaults(command=self.run)