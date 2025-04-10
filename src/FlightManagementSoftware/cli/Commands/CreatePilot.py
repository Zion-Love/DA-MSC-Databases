from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertStringNotEmpty,
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.CommandHandler import CommandHandler

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
        if(self.airlineId != None):
            self.airlineId = AssertIsPositiveInteger(self.airlineId)


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
        parser.add_argument('--name', type=str, help='New pilots name')
        parser.add_argument('--airlineId', nargs='?', type=int, help='New pilots name')
        parser.set_defaults(command=self.run)