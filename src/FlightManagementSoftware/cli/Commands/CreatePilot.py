from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertStringNotEmpty,
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import (
    AbortCommandException,
    ContinueYN
)

'''
    This Command will Add a new Pilot to our system

    Requires:
        Name : the name of the pilot
        airlineId : int
'''

@dataclass
class CreatePilotCommand(CommandHandler):
    name : str
    airlineId : int = None


    def Validate(self):
        self.name = AssertStringNotEmpty(self.name)
        if self.airlineId != None:
            self.airlineId = AssertIsPositiveInteger(self.airlineId)

            self.existingAirline : Airline = Airline.QueryById(self.airlineId)

            if self.existingAirline == None:
                raise AbortCommandException(f"Airline with Id {self.airlineId} could not be found")
            if self.existingAirline.DeletedDate == None:
                ContinueYN("WARNING: Creating a pilot for a deleted airline, Continue ? (y/n)")


    def Handle(self):
        pilot : Pilot = Pilot(
            Id=None,
            Name=self.name,
            AirlineId=self.airlineId,
            CreatedDate=datetime.now(),
            DeletedDate=None)
        pilot.Create()
        print(f"Pilot successfully created {pilot}")
        

class CreatePilotCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreatePilotCommand)


    def BuildCommandArgs(self, parser : ArgumentParser):
        parser.add_argument('--name', type=str, help='New pilots name', required=True)
        parser.add_argument('--airlineId', nargs='?', type=int, help="The AirlineId that the pilot works for")
        parser.set_defaults(command=self.run)