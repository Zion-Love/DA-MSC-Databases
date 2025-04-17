from dataclasses import dataclass
from FlightManagementSoftware.Entities.Airline import Airline
from FlightManagementSoftware.Entities.Pilot import Pilot
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN, AbortCommandException

'''
    This Command will delete an Airline and unassign any Pilots from it
'''

@dataclass
class DeleteAirlineCommand(CommandHandler):
    airlineId : int

    def Validate(self):
        self.airline : Airline = Airline.QueryById(self.airlineId)

        if self.airline == None:
            raise AbortCommandException(f"Could not find airline with Id {self.airline}")
        self.assignedPilots = Pilot.QueryByAirline(self.airlineId)

        if self.assignedPilots != None:
            ContinueYN(f"WARNING: Deleting this airline will un-assign {len(self.assignedPilots)} pilots , continue? (y/n)")


    def Handle(self):
        self.airline.Delete()

        if self.assignedPilots != None:
            for pilot in self.assignedPilots:
                pilot.AirlineId = None
                pilot.Update()

        print(f"Successfully Deleted Airlaine with Id {self.airlineId}")


class DeleteAirlineCommandParser(CommandParser):

    def __init__(self,):
        super().__init__(DeleteAirlineCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-a","-aId","--airlineId", type=int, required=True, help="The Id of the Airline to delete")
        parser.set_defaults(command=self.run)