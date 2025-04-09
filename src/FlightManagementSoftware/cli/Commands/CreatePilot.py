from argparse import ArgumentParser
from dataclasses import dataclass
from FlightManagementSoftware.cli.InputValidator import (
    AssertStringNotEmpty
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.CommandHandler import CommandHandler

'''
    This Command will Add a new Pilot to our system

    Requires:
        Name : the name of the pilot
'''

@dataclass
class CreatePilotCommand(CommandHandler):
    name : str
    airlineId : int = None

    def Validate(self):
        self.name = AssertStringNotEmpty(self.name)

    def Handle(self):
        pilot : Pilot = Pilot(Name=self.name)
        pilot.Create()
        print(f"Pilot successfully created with Id : {pilot.Id} : ")
        print(pilot)
        

class CreatePilotCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreatePilotCommand)

    def BuildCommandArgs(self, parser : ArgumentParser):
        parser.add_argument('--name', type=str, help='New pilots name')
        parser.set_defaults(command=self.run)


CreatePilotCommand(**{"name" : "test"})