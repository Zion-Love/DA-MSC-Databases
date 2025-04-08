from InputValidator import (
    AssertStringNotEmpty
)
import CommandHandler
from CommandParser import CommandParser
from Entities.Pilot import Pilot
from argparse import ArgumentParser
from dataclasses import dataclass

'''
    This Command will Add a new Pilot to our system

    Requires:
        Name : the name of the pilot
'''

@dataclass
class CreatePilotCommand(CommandHandler):
    Name : str

    def Validate(self):
        self.Name = AssertStringNotEmpty(self.Name)

    def Handle(self):
        pilot : Pilot = Pilot(Name=self.Name)
        pilot.Create()
        print(f"Pilot successfully created with Id : {pilot.Id} : ")
        print(pilot)
        

class CreatePilotCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreatePilotCommand)


    def BuildCommandArgs(self, parser : ArgumentParser):
        parser.add_argument('--name', type=str, help='New pilots name')
        parser.set_defaults(command=self.run)

