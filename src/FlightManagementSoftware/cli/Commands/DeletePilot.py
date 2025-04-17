from argparse import ArgumentParser
from dataclasses import dataclass
from FlightManagementSoftware.cli.InputValidator import (
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException

'''
    This Command will Delete an existing pilot from the system.

    Requires:
        - pilotId
'''
@dataclass
class DeletePilotCommand(CommandHandler):
    pilotId : str


    def Validate(self):
        self.pilotId = AssertIsPositiveInteger(self.pilotId)
        self.existingPilot : Pilot = Pilot.QueryById(self.pilotId)

        if self.existingPilot == None:
            raise AbortCommandException(f"No pilot with Id : {self.pilotId}")
        if self.existingPilot.DeletedDate != None:
            raise AbortCommandException(f"Pilot with Id : {self.pilotId} has already been deleted")


    def Handle(self):
        self.existingPilot.Delete()
        print(f"Pilot with Id {self.pilotId} Successfully Deleted")
        

class DeletePilotCommandParser(CommandParser):
    def __init__(self):
        super().__init__(DeletePilotCommand)


    def BuildCommandArgs(self, parser : ArgumentParser):
        parser.add_argument('-id','-p','--pilotId',nargs=None, type=int, help='Id of the pilot to delete', required=True)
        parser.set_defaults(command=self.run)