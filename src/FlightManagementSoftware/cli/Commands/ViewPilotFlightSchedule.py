from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertIsPositiveInteger,
    AssertDateTimeString
)
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.repositories.PilotRepository import pilotRepository
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException



'''
    This command will View a specific Pilot(s) Flight Schedule

    can be filtered by :
    - includeDeleted
    - startDate : Where DepartureTimeUTC >= startDate
    - endDate : Where DepartureTimeUTC <= endDate
'''

@dataclass
class ViewPilotFlightScheduleCommand(CommandHandler):
    startDate : datetime = datetime.now()
    pilotId : int = None
    endDate : datetime = None
    includeDeleted : bool = False


    def Validate(self):
        if self.endDate != None: assert(self.startDate < self.endDate)

        if self.pilotId != None: 
            if isinstance(self.pilotId,int):
                self.pilotId = AssertIsPositiveInteger(self.pilotId)
            elif isinstance(self.pilotId, list):
                self.pilotId = [AssertIsPositiveInteger(i) for i in self.pilotId]

        if self.startDate != None and self.endDate != None:
            if self.startDate > self.endDate:
                raise AbortCommandException(f"startDate : {self.startDate} cannot be after endDate : {self.endDate}")


    def Handle(self):
        flightScheduleInformation : DataFrame = None

        flightScheduleInformation = (
            pilotRepository
            .QueryPilotFlightSchedule(
                pilotId=self.pilotId,
                includeDeletedFlights=self.includeDeleted,
                startDate=self.startDate,
                endDate=self.endDate
            )
        )
        print(flightScheduleInformation)


class ViewPilotFlightScheduleCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewPilotFlightScheduleCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('-p','--pilotId', nargs='+', type=int, help="The pilotId whose schedule to view", required=True)

        parser.add_argument('-s','-from','-begin','-start','--startDate', nargs='?', 
            type=lambda x: AssertDateTimeString(x),
            help="The start date to view the schedule from")
        
        parser.add_argument('-e','-to','-finish','-end','--endDate', nargs='?', 
            type=lambda x: AssertDateTimeString(x), 
            help="The end date to view the schedule to")
        
        parser.add_argument('-del','-includeDeleted', action='store_true',help="Toggle to include deleted flights")
        parser.set_defaults(command=self.run)
