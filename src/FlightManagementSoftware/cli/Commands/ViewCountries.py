from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.Entities.Country import Country

'''
    This Command will View the countries supported by the system

    Can be filtered by 
    - includeInactive : if present will show Countries that have AllowingFlights = 1
    - includeDeleted : if present will also show soft deleted countries
'''

@dataclass
class ViewCountriesCommand(CommandHandler):
    includeInactive : bool = False
    includeDeleted  : bool = False

    def Validate(self):
        pass


    def Handle(self):
        countries = Country.Query(self.includeDeleted, self.includeInactive)
        print(countries)

        
class ViewCountriesCommandParser(CommandParser):
    def __init__(self):
        super().__init__(ViewCountriesCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-ii","-incInactive", "--includeInactive", action='store_true', help="If Supplied will also show Countries that are not allowing flights currently")
        parser.add_argument("-id","-incDeleted", "--includeDeleted", action='store_true', help="If Supplied will also show Countries that have been soft deleted")
        parser.set_defaults(command=self.run)
