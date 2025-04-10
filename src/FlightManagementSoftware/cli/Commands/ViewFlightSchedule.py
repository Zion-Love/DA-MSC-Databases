from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import AssertIsPositiveInteger
from FlightManagementSoftware.repositories.FlightRepository import flightRepository
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser

'''
    This command will query for flight schedules with aggregated pilot information

    can be filtered by:
        - pilotId : Either as a list or as a singular integer
        - flightId : Either as a list or as a singular integer
        - includeCompleted
        - includeDeleted
    
'''

@dataclass
class ViewFlightScheduleCommand(CommandHandler):
    pilotId : int | list[int] = None
    flightId : int | list[int] = None
    destinationId : int | list[int] = None
    DepartureDateUTC : datetime = None
    includeCompelted : bool = False # clasified as ArrivalTimeUTC is NULL
    includeDeleted : bool = False

    def Validate(self):
        # validate all pilot ids are +ve 
        if self.pilotId != None:
            if isinstance(self.pilotId, list):
                self.pilotId = [AssertIsPositiveInteger(id) for id in self.pilotId]
            else: self.pilotId = AssertIsPositiveInteger(self.pilotId)

        # validate all flight ids are +ve
        if self.flightId != None:
            if isinstance(self.flightId, list):
                self.flightId = [AssertIsPositiveInteger(id) for id in self.flightId]
            else: self.flightId = AssertIsPositiveInteger(self.flightId)

    
    def Handle(self):
        flights = flightRepository.QueryByPilotFlight(
            pilotId=self.pilotId, 
            flightId=self.flightId,
            includeDeleted=self.includeDelete)
        print(flights)


class ViewFlightScheduleCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewFlightScheduleCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("--pilotId", nargs='*', type=int, help="PilotIds to filter for.")
        parser.add_argument("--flightId", nargs='*', type=int, help="FlightIds to filter for.")
        parser.add_argument("-includeDeleted", action='store_true', help="If set will also show deleted Flights")
        parser.add_argument("-includeCompleted", action='store_true', help="If set will also show completed flights (flights with an ArrivalDateUTC)")
        parser.set_defaults(command=self.run)
    