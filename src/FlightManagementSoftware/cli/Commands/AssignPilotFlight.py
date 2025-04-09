from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.PilotFlight import PilotFlight
from FlightManagementSoftware.cli.CommandHandler import CommandHandler

'''
    This command will assign a pilot to a flight

    REQUIRES:
        - pilotId
        - flightId
'''

@dataclass
class AssignPilotFlightCommand(CommandHandler):
    pilotId : int
    flightId : int

    # no need to validate these Id's here since the FK constraint will validate they exist
    def Validate(self):
        pass

    def Handle(self):
        pilotFlight : PilotFlight = PilotFlight(PilotId=self.pilotId,FlightId=self.flightId)
        pilotFlight.Create()
        print("Pilot successfully assigned to flight")


class AssignPilotFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(AssignPilotFlightCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('--pilotId', type=int, help="The pilotId to assign")
        parser.add_argument('--flightId', type=int, help="the flightId to assign to")