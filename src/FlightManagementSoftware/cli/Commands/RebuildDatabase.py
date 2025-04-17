from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.db.sqlite import dbConnectionInstance

'''
    This command will wipe the database and rebuild it from the CreateTestData.sql file
    effectively allowing the user to mutate the db data as much as they like through the provided cli commands
    whilst giving the ability to rollback to the base state whenevr they so wish

    it was very usefull whilst developing this piece of software.
'''
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