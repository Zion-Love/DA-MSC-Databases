from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException, ContinueYN

'''
    This command will Update a Pilots Information
'''

@dataclass
class UpdatePilotCommand(CommandHandler):
    pilotId : int
    name : str = None
    airlineId : int = None
    undoDeletion : bool = False

    def Validate(self):
        self.pilot : Pilot = Pilot.QueryById(self.pilotId)
        self.airline = None

        if self.pilot == None:
            raise AbortCommandException(f"Could not find Pilot with Id : {self.pilotId}")
        
        if self.pilot.DeletedDate != None:
            ContinueYN("WARNING: Updating data for a deleted Pilot, Continue? (y/n)")

        if self.airlineId != None:
            self.airline : Airline = Airline.QueryById(self.airlineId)

            if self.airline == None:
                raise AbortCommandException(f"Could not find Airline with Id {self.airlineId}")
            
            if self.airline.DeletedDate != None:
                raise AbortCommandException(f"Airline with Id : {self.airlineId} is deleted, cannot be assigned to a pilot")


    def Handle(self):
        if self.name != None:
            self.pilot.Name = self.name
        if self.airline != None:
            self.pilot.AirlineId = self.airline.Id
        if self.undoDeletion == True:
            self.pilot.DeletedDate = None
        self.pilot.Update()
        print(f"Successfully updated Pilot : {self.pilot}")


class UpdatePilotCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdatePilotCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-p", "-pId", "--pilotId", type=int, required=True, help="The Id of the Pilot to Update")
        parser.add_argument("-n","--name", type=str, help="The name of the pilot")
        parser.add_argument("-a","-aId","--airlindId", type=int, help="The Id of the Airline that employes the pilot")
        parser.add_argument("-ud","--undoDeletion", action="store_true", help="If included will undo the deletion of a Pilot")
        parser.set_defaults(command=self.run)