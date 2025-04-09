from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.db.sqlite import dbConnectionInstance

# this command is used to buildup the test database with the DDL and data isnerts 
# from the CreateTestData.sql file
@dataclass
class RebuildDatabaseCommand(CommandHandler):
    def Validate(self):
        pass

    def Handle(self):
        dbConnectionInstance.Init_db(refresh=True)


class RebuildDatabaseCommandParser(CommandParser):
    def __init__(self):
        super().__init__(RebuildDatabaseCommand)

    def BuildCommandArgs(self, parser):
        parser.set_defaults(command=self.run)