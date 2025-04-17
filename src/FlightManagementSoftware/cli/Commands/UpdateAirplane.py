from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airplane import Airplane
from FlightManagementSoftware.Entities.Destination import Destination
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException, ContinueYN
from FlightManagementSoftware.cli.InputValidator import AssertDateTimeString

'''
    This Command will Update an Airplanes Data

    Id : int
    ModelNumber : str
    ManufacturedDate : datetime
    LastServiceDate : datetime
    PassengerCapacity : int
    CurrentDestinationId : int
    CreatedDate : datetime
    DeletedDate : datetime
'''

@dataclass
class UpdateAirplaneCommand(CommandHandler):
    airplaneId : int
    modelNumber : str = None
    manufacturedDate : datetime = None
    lastServiceDate : datetime = None
    passengerCapacity : int = None
    currentDestinationId : int = None
    undoDeletion : bool = False

    def Validate(self):
        self.airplane : Airplane = Airplane.QueryById(self.airplaneId)
        self.currentDestination = None

        if self.currentDestinationId != None:
            self.currentDestination : Destination = Destination.QueryById(self.currentDestinationId)

            if self.currentDestination == None:
                raise AbortCommandException(f"Failed to find Destination with Id :{self.currentDestinationId}")

        if self.airplane == None:
            raise AbortCommandException(f"Could not find Airplane with Id : {self.airplaneId}")
        
        if self.airplane.DeletedDate != None:
            ContinueYN(f"WARNING: Updating data for a deleted Airplane, Continue? (y/n)")


    def Handle(self):
        if self.modelNumber != None:
            self.airplane.ModelNumeber = self.modelNumber
        if self.manufacturedDate != None:
            self.airplane.ManufacturedDate = self.manufacturedDate
        if self.lastServiceDate != None:
            self.airplane.LastServiceDate = self.lastServiceDate
        if self.passengerCapacity != None:
            self.airplane.PassengerCapacity = self.passengerCapacity
        if self.currentDestination != None:
            self.airplane.CurrentDestinationId = self.currentDestination.Id
        if self.undoDeletion == True:
            self.airplane.DeletedDate = True
        self.airplane.Update()
        print(f"Successfully Updated Airplane : {self.airplane}")


class UpdateAirplaneCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateAirplaneCommand)

    
    def BuildCommandArgs(self, parser):
        parser.add_argument("-a","-aId","-plane","--airplaneId", type=int, required=True, help="The Id of the Airplane to Update")
        parser.add_argument("-n", "-model", "--modelNumber", type=str, help="The Model Number of the plane")
        parser.add_argument("-m","-mDate","--manufacturedDate", type=lambda x: AssertDateTimeString(x), help="The Manufacture Date of the Airplane")
        parser.add_argument("-ls", "-lsDate","--service","--lastServiceDate", type=lambda x: AssertDateTimeString(x), help="The Last Service Date of the Airplane")
        parser.add_argument("-d","-dId","-currentLocation", "-dest", "--currentDestinationId", type=int, help="The Destination Id the Airplane is Currently at")
        parser.add_argument("-ud","-undoDel","--undoDeletion", action="store_true", help="If Included will undo the deletion of an Airplane")
        parser.set_defaults(command=self.run)