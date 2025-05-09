from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.PilotFlight import PilotFlight
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN, AbortCommandException

'''
    This command will assign a pilot to a flight

    it will handle adding pilots to deleted flight but only after warning and confirming with the user.

    REQUIRES:
        - pilotId
        - flightId

    OPTIONAL:
        - remove : flag to determine operation is adding a new pilot flight assignment or removing an existing one
'''

@dataclass
class AssignPilotFlightCommand(CommandHandler):
    pilotId : int
    flightId : int
    remove : bool = False

    def Validate(self):
        self.pilot : Pilot = Pilot.QueryById(self.pilotId)
        self.flight : Flight = Flight.QueryById(self.flightId)

        if self.flight.DeletedDate != None or self.flight.ArrivalTimeUTC != None:
            ContinueYN("WARNING: Attempting to modify a pilot assignment for a deleted or completed flight, Continue? (y/n)",)

        if self.pilot.DeletedDate != None:
            if self.flight.DeletedDate != None or self.flight.ArrivalTimeUTC != None:
                ContinueYN("WARNING: Attempting to modify a deleted pilot assignment, Continue? (y/n)")
            else:
                raise AbortCommandException("Cannot add a deleted pilot to an active flight")
            

    def Handle(self):
        if self.remove == False:
            self._HandleAddPilot()
        else:
            self._HandleRemovePilot()


    def _HandleAddPilot(self):
        existingAssigment : PilotFlight = PilotFlight.QueryPilotFlight(pilotId=self.pilotId, flightId=self.flightId)

        # guard statement if already added to flight
        if existingAssigment:
            raise AbortCommandException(f"Pilot : {f'{self.pilot.Name} (Id:{self.pilot.Id})'} already assigned to flight  (Id:{self.flight.Id})")
 
        pilotFlight : PilotFlight = PilotFlight(PilotId=self.pilotId,FlightId=self.flightId)
        try:
            pilotFlight.Create()
            print(f"Pilot : {f'{self.pilot.Name} (Id:{self.pilot.Id})'} successfully assigned to flight (Id:{self.flight.Id})")
        except Exception as e:
            raise AbortCommandException(f"Could not complete request : {e}")


    def _HandleRemovePilot(self):
        existingAssigment : PilotFlight = PilotFlight.QueryPilotFlight(pilotId=self.pilotId, flightId=self.flightId)

        # guard statement if nothing to remove
        if existingAssigment == None:
            print("Pilot is not currenly assigned to that flight")
            return
        
        PilotFlight.Delete(pilotId=existingAssigment.PilotId, flightId=existingAssigment.FlightId)
        print(f"Pilot : {f'{self.pilot.Name} (Id:{self.pilot.Id})'} successfully removed from flight (Id:{self.flight.Id})")



class AssignPilotFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(AssignPilotFlightCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('-p','--pilotId', type=int, required=True, help="The pilotId to assign")
        parser.add_argument('-f','--flightId', type=int, required=True, help="the flightId to assign to")
        parser.add_argument('-r','--remove', action='store_true', help="Specifies to remove the pilot assignment")
        parser.set_defaults(command=self.run)