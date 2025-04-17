from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Country import Country
from FlightManagementSoftware.Entities.Destination import Destination
from FlightManagementSoftware.Entities.Flight import Flight
from FlightManagementSoftware.Entities.FlightPath import FlightPath
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException, ContinueYN


@dataclass
class DeleteCountryCommand(CommandHandler):
    countryId : int

    def Validate(self):
        self.country : Country = Country.QueryById(self.countryId)

        if self.country == None:
            raise AbortCommandException(f"Could not find Country with Id : {self.countryId}")
        if self.country.DeletedDate != None:
            raise AbortCommandException(f"Country with Id : {self.countryId} has already been deleted")
        
        destinations = Destination.QueryByCountry(self.countryId)
        flightPaths = FlightPath.QueryByCountry(self.countryId)
        flights = Flight.QueryPendingByCountry(self.countryId)

        if destinations == None and flightPaths == None and flights == None:
            return
        
        warning = "WARNING: Deleting this destination will also delete "

        if destinations != None: warning += f"{len(destinations)} Destination(s)"
        if flightPaths != None: warning += f", {len(flightPaths)} FlightPaths(s)"
        if flights != None: warning += f", {len(flights)} Flight(s)"

        warning += " Continue? (y/n)"

        ContinueYN(warning)


    def Handle(self):
        self.country.Delete()
        print("Country successfully deleted")


class DeleteCountryCommandParser(CommandParser):
    def __init__(self):
        super().__init__(DeleteCountryCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-c","-cId","--countryId", type=int, required=True, help="The Id of the Country to Delete")
        parser.set_defaults(command=self.run)