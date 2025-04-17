from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airplane import Airplane
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This command will create a new Airplane using the supplied data
'''
@dataclass
class CreateAirplaneCommand(CommandHandler):
    modelNumber : str
    manufacturedDate : datetime
    lastServiceDate : datetime
    passengerCapacity : int
    currentDestinationId : int = None
    currentDestinationAirportCode : str = None

    def Validate(self):
        if self.lastServiceDate > datetime.now():
            raise AbortCommandException("LastServiceDate is invalid")
        if self.manufacturedDate > datetime.now():
            raise AbortCommandException("Manufactored date is invalid")
        
        self.currentDestinationId = None
        if self.currentDestinationId != None or self.currentDestinationAirportCode != None:
            currentDestination : Destination = (
                Destination.QueryById(self.currentDestinationId) if self.currentDestinationId != None else
                Destination.QueryByAirportCode(self.currentDestinationAirportCode)
            )

            if currentDestination == None:
                raise AbortCommandException(f"Could not find destination")
            
            self.currentDestinationId = currentDestination.Id


    def Handle(self):
        airplane : Airplane = Airplane(
            Id=None,
            ModelNumeber=self.modelNumber,
            ManufacturedDate=self.manufacturedDate,
            LastServiceDate=self.lastServiceDate,
            PassengerCapacity=self.passengerCapacity,
            CurrentDestinationId=self.currentDestinationId,
            CreatedDate=datetime.now(),
            DeletedDate=None
        )
        airplane.Create()
        print(f"Airplane Successfully Create : {airplane}")


class CreateAirplaneCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateAirplaneCommand)


    def BuildCommandArgs(self, parser):
        parser.set_defaults(command=self.run)