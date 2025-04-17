from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Country import Country
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException, ContinueYN

@dataclass
class UpdateCountryCommand(CommandHandler):
    countryId : int = None
    isoCode : str = None
    name : str = None
    setAllowingFlights : bool = None
    setNotAllowingFlights : bool = None
    undoDeletion : bool = None


    def Validate(self):
        if self.setAllowingFlights == True and self.setNotAllowingFlights == True:
            raise AbortCommandException("Ambiguous use of setAllowingFlights and setNotAllowingFlights, please only provide one or none")

        self.country : Country = Country.QueryById(self.countryId)

        if self.country == None:
            raise AbortCommandException(f"Could not find Country with Id : {self.countryId}")
        
        if self.isoCode != None:
            existingIsoCode : Country = Country.QueryByIsoCode(self.isoCode)
            if existingIsoCode != None:
                raise AbortCommandException(f"A Country with IsoCode : {self.isoCode} already exists With Id {existingIsoCode.Id}")
        
        if self.country.DeletedDate != None:
            ContinueYN("WARNING: Edditing data for a deleted Country, Continue? (y/n)")


    def Handle(self):
        if self.isoCode != None:
            self.country.IsoCode = self.isoCode
        if self.name != None:
            self.country.Name = self.name
        if self.undoDeletion and self.country.DeletedDate != None:
            self.country.DeletedDate = None

        if self.setAllowingFlights:
            self.country.AllowingFlights = True
        elif self.setNotAllowingFlights:
            self.country.AllowingFlights = False

        self.country.Update()

        print(f"Successfully updated Country : {self.country}")


class UpdateCountryCommandParser(CommandParser):

    def __init__(self):
        super().__init__(UpdateCountryCommand)

    def BuildCommandArgs(self, parser):
        parser.add_argument("-c","-id","-cId","--countryId", type=int, required=True, help="The Id of the Country to update")
        parser.add_argument("-n","--name", type=str, help="The Name of the Country")
        parser.add_argument("-code","--isoCode", type=str, help="The IsoCode of the Country")
        parser.add_argument("-f","--flights","--setAllowingFlights", action='store_true', help="If included will set the Country to AllowingFlights = True")
        parser.add_argument("-nf","--noFlight","--setNotAllowingFlights", action='store_true', help="If included will set the Country to AllowingFlights = True")
        parser.add_argument("-ud","-undoDel","--undoDeletion", action='store_true', help="If included will undo the deletion of a Country")
        parser.set_defaults(command=self.run)