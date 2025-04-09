from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertIsPositiveInteger
)
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.repositories.PilotRepository import pilotRepository
from FlightManagementSoftware.cli import CommandParser

'''
    Request to view a secific pilots flight schedule, requires the pilotId
'''
@dataclass
class ViewPilotFlightScheduleCommand(CommandHandler):
    pilotId : int
    startDate : datetime
    endDate : datetime = None
    includeDeletedFlights : bool = False


    def Validate(self):
        assert(self.startDate < self.endDate)
        assert(isinstance(self.pilotId, int) and self.pilotId != None)
        self.pilotId = AssertIsPositiveInteger(self.pilotId)


    def Handle(self):
        flightScheduleInformation : DataFrame = (
            pilotRepository
            .QueryPilotFlightSchedule(
                self.pilotId,
                self.includeDeletedFlights,
                self.startDate,
                self.endDate
            )
        )
        print(flightScheduleInformation)


class ViewPilotFlightScheduleCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewPilotFlightScheduleCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('--pilotId', type=int, help="The PilotId to view flights for")
        parser.set_defaults(command=self.run)