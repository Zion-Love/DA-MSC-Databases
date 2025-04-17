from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.Entities.Country import Country
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser

'''
    This Command will create a new Country record using the supplied data
'''
@dataclass
class CreateCountryCommand(CommandHandler):
    isoCode : str
    name : str
    notAllowingFlights : bool = False

    def Validate(self):
        pass


    def Handle(self):
        country : Country = Country (
            Id=None,
            IsoCode=self.isoCode,
            Name=self.name,
            AllowingFlights=not self.notAllowingFlights,
            CreatedDate=datetime.now(),
            DeletedDate=None
        )
        country.Create()
        print(f"Successfully created Country : {country}")


class CreateCountryCommandParser(CommandParser):
    def __init__(self):
        super().__init__(CreateCountryCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument("-n","--name", type=str, required=True, help="The Name of the country")
        parser.add_argument("-c","-code","--isoCode" , type=str, required=True, help="The Iso Code of the country I.E GB for great britain")
        parser.add_argument("-nf","-noFlights","--notAllowingFlights", action='store_true', help="If included will set the AllowingFlights flag to False for thr=e created country")
        parser.set_defaults(command=self.run)