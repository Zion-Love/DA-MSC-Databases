from dataclasses import dataclass
from FlightManagementSoftware.Entities.Airplane import Airplane
from FlightManagementSoftware.repositories.FlightRepository import flightRepository
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN , AbortCommandException

'''
    This command will soft delete an airplane
'''
@dataclass
class DeleteAirplaneCommand(CommandHandler):
    airplaneId : int
    
    def Validate(self):
        self.airplane : Airplane = Airplane.QueryById(self.airplaneId)

        if self.airplane == None:
            raise AbortCommandException(f"Could not find airplane with Id : {self.airplaneId}")
        
        if self.airplane.DeletedDate != None:
            raise AbortCommandException(f"Airplane with Id : {self.airplaneId} has already been deleted")
        
        pendingFlights = flightRepository.QueryByAirplane(self.airplane,True,True)

        if pendingFlights != None:
            ContinueYN(f"WARNING: This airplane has {len(pendingFlights.data)} pending flights, deleting it will also delete all of these flights, continue? (y/n)")


    def Handle(self):
        self.airplane.Delete()
        print(f"Succesfully deleted Airplane with Id: {self.airplaneId}")


class DeleteAirplaneCommandParser(CommandParser):

    def __init__(self):
        super().__init__(DeleteAirplaneCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-a","-aId","--airplaneId", required=True, help="The Id of the Airplane to delete")
        parser.set_defaults(command=self.run)