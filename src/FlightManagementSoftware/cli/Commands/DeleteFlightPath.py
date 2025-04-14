from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.InputValidator import (
    AssertStringNotEmpty,
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.repositories.FlightRepository import flightRepository
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import (
    AbortCommandException,
    ContinueYN
)
from FlightManagementSoftware.DataTransferObjects import DataFrame

'''
    This command will delete flight paths(s) from the system, it will also delete any pending flights associated
    with the deleted flight path
'''


@dataclass
class DeleteFlightPathCommand(CommandHandler):
    flightPathId : int

    def Validate(self):
        self.flightPathId = AssertIsPositiveInteger(self.flightPathId)

        self.existingFlightPath : FlightPath = FlightPath.QueryById(self.flightPathId)

        if self.existingFlightPath == None:
            raise AbortCommandException(f"No existing flight path with Id : {self.flightPathId}")
        
        if self.existingFlightPath.DeletedDate != None:
            raise AbortCommandException(f"Flight path with Id : {self.flightPathId} has already been deleted.")
        

        self.pendingFlights : DataFrame = flightRepository.QueryScheduleByFlightPath(self.flightPathId, False)

        if self.pendingFlights != None:
            print(self.pendingFlights)
            ContinueYN("WARNING: Deleting this flight path will also delete all of the above pending flights, continue? (y/n)")
    

    def Handle(self):
        Flight.DeleteById([flight.Id for flight in self.pendingFlights.data])
        self.existingFlightPath.Delete()
        print(f"FlightPath with Id : {self.existingFlightPath} successfully deleted")


class DeleteFlightPathCommandParser(CommandParser):
    def __init__(self):
        super().__init__(DeleteFlightPathCommand)

    
    def BuildCommandArgs(self, parser):
        parser.add_argument('-fp','-id','--flightPathId',nargs=None, required=True, help="The Id of the flight path to delete")
        parser.set_defaults(command=self.run)
