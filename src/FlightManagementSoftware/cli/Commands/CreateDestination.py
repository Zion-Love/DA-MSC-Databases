from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException
from FlightManagementSoftware.Entities.Country import Country
from FlightManagementSoftware.Entities.Destination import Destination


'''
    This command will Create a new Destination using the supplied data
'''
@dataclass
class CreateDestinationCommand(CommandHandler):
    name : str
    airportCode :str
    inactive : bool
    countryId : int = None
    countryCode : str = None

    def Validate(self):
        if self.countryCode == None and self.countryId == None:
            raise AbortCommandException("You must suspsply either a coutnry Id or a country code")
    
        if self.countryCode != None:
            self.country : Country = Country.QueryByIsoCode(self.countryCode)

            if self.country == None:
                raise AbortCommandException(f"Could not find country with IsoCode : {self.countryCode}")
            
        elif self.countryId != None:
            self.country : Country = Country.QueryById(self.countryId)

            if self.country == None:
                raise AbortCommandException(f"Could not find country with Id : {self.countryId}")


    def Handle(self):
        destination : Destination = Destination(
            Id=None,
            CountryId=self.country.Id,
            Name=self.name,
            AirportCode=self.airportCode,
            Active=not self.inactive,
            CreatedDate=datetime.now(),
            DeletedDate=None)
        destination.Create()
        print(f"Successfully created Destination : {destination}")


class CreateDestinationCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateDestinationCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-cId","--countryId",nargs=None, type=int, help="The CountryId the Destination resides in")
        parser.add_argument("-ccode","--countyCode", nargs=None, type=str, help="The Country IsoCode the Destination resides in")
        parser.add_argument('-n',"--name", type=str, help="", required=True)
        parser.add_argument("-ac","-airport","--airportCode", type=str, help="The Airport Code for the destination")
        parser.add_argument("-i","--inactive", action='store_true', help="Create the destination as inactive")
        parser.set_defaults(command=self.run)