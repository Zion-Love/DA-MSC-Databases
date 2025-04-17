from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException, ContinueYN

'''
    This Commmand will delete a Flight
'''


@dataclass
class DeleteFlightCommand(CommandHandler):
    flightId : int

    def Validate(self):
        self.flight : Flight = Flight.QueryById(self.flightId)

        if self.flight == None:
            raise AbortCommandException(f"Could not find Flight with Id : {self.flightId}")
        if self.flight.DeletedDate != None:
            raise AbortCommandException(f"Flight with Id : {self.flightId} has already been deleted")


    def Handle(self):
        self.flight.Delete()
        print(f"Successfully Deleted flight with Id : {self.flightId}")


class DeleteFlightCommandParser(CommandParser):
    def __init__(self):
        super().__init__(DeleteFlightCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-f","--flightId", type=int, required=True, help="The Id of the flight to delete")
        parser.set_defaults(command=self.run)