from dataclasses import dataclass
from FlightManagementSoftware.cli.InputValidator import (
    AssertDateTimeString,
    AssertDateAIsBeforeDateB,
    AssertIsPositiveInteger
)
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.cli.UserInputHelpers import ContinueYN
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This command provides a way to update information about a specific flight path

    Intentionally not allowing the editing of the CreatedDate column as this is representative
    of the insertion time of record
'''
@dataclass
class UpdateDestinationCommand(CommandHandler):
    destinationId : int


    def Validate(self):
        self.existingDestination = Destination.QueryById(self.destinationId)

        if self.existingDestination == None:
            raise AbortCommandException(f"Could not find desitnation with Id : {self.destinationId}")


    def Handle(self):
        pass


class UpdateDestinationCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateDestinationCommand)


    # TODO :
    def BuildCommandArgs(self, parser):
        parser.add_argument('-d','-dest',"--destinationId", type=lambda x: AssertIsPositiveInteger(x), nargs=None, help="The Destination Id to update data for", required=True)

        parser.set_defaults(command=self.run)
