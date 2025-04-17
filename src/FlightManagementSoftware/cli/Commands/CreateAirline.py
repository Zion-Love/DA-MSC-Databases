from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.cli.InputValidator import AssertStringNotEmpty
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser

'''
    This Command will create a new Airline with the supplied data
'''
@dataclass
class CreateAirlineCommand(CommandHandler):
    name : str

    def Validate(self):
        self.name = AssertStringNotEmpty(self.name)
    
    
    def Handle(self):
        airline : Airline = Airline(
            Id=None,
            Name=self.name,
            CreatedDate=datetime.now(),
            DeletedDate=None
        )
        airline.Create()
        print(f"Successfully created Airline : {airline}")


class CreateAirlineCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateAirlineCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-n","--name", type=str, required=True, help="The name of the Airline")
        parser.set_defaults(command=self.run)