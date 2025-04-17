from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN

'''
    This Command will Update an Airline record using the supplied data

    Id : int
    Name : str
    CreatedDate : datetime
    DeletedDate : datetime
'''
@dataclass
class UpdateAirlineCommand(CommandHandler):
    airlineId : int
    name : str = None
    undoDeletion : bool = False


    def Validate(self):
        self.airline : Airline = Airline.QueryById(self.airlineId)

        if self.airline == None:
            raise AbortCommandException(f"Could not find Airline with Id : {self.airlineId}")
        
        if self.name == None and (self.undoDeletion == False or self.name == self.airline.Name):
            raise AbortCommandException(f"Nothing to update")
        
        if self.airline.DeletedDate != None:
            ContinueYN("WARNING: Updating data for a deleted Airline, Continue? (y/n)")


    def Handle(self):
        if self.name != None:
            self.airline.Name = self.name

        if self.undoDeletion and self.airline.DeletedDate != None:
            self.airline.DeletedDate = None
        
        self.airline.Update()
        print(f"Successfully updated Airline : {self.airline}")


class UpdateAirlineCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateAirlineCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-a","-aId","--airlineId", type=int, required=True, help="The Id of the Airline to Update")
        parser.add_argument("-n", "--name", type=str, help="The Name of the Airline")
        parser.add_argument("-ud","-uDel","--undoDeletion", action="store_true", help="If included will undo the deletion of an Airline")
        parser.set_defaults(command=self.run)