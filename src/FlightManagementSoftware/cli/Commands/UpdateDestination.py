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
from FlightManagementSoftware.Entities.Country import Country
from FlightManagementSoftware.Entities.Destination import Destination

'''
    This command provides a way to update information about a specific flight path

    Intentionally not allowing the editing of the CreatedDate column as this is representative
    of the insertion time of record


       Id : int
    CountryId : int
    Name: str
    AirportCode: str
    Active: bool
    CreatedDate: datetime
    DeletedDate: datetime
'''
@dataclass
class UpdateDestinationCommand(CommandHandler):
    destinationId : int
    countryId : int = None
    countryCode : str = None
    name : str = None
    airportCode : str = None
    setActive : bool = False
    setInactive : bool = False
    undoDeletion : bool = False

    def Validate(self):
        if self.setActive and self.setInactive:
            raise AbortCommandException("You can only supply one or none of setActive and setInactive")
        self.existingDestination : Destination = Destination.QueryById(self.destinationId)
        self.newCountry : Country = None

        if self.existingDestination == None:
            raise AbortCommandException(f"Could not find desitnation with Id : {self.destinationId}")
        
        if self.countryId != None or self.countryCode != None:
            self.newCountry = (
                Country.QueryById(self.countryId) if self.countryId != None else
                Country.QueryByIsoCode(self.countryCode)                                  
            )

            if self.newCountry == None:
                raise (
                    AbortCommandException(f"Could not find country with Id : {self.countryId}") if self.countryId != None else
                    AbortCommandException(f"Could not find country with IsoCode : {self.countryCode}")
                )
            
    
    def Handle(self):
        if self.newCountry != None:
            self.existingDestination.CountryId = self.newCountry.Id
        if self.name != None:
            self.existingDestination.Name = self.name
        if self.airportCode != None:
            self.existingDestination.AirportCode = self.airportCode
        if self.undoDeletion:
            self.existingDestination.DeletedDate = None
        if self.setActive:
            self.existingDestination.Active = True
        if self.setInactive:
            self.existingDestination.Active = False

        self.existingDestination.Update()
        print(f"Sucessfully updated Destination : {self.existingDestination}")


class UpdateDestinationCommandParser(CommandParser):
    def __init__(self):
        super().__init__(UpdateDestinationCommand)


    def BuildCommandArgs(self, parser):
        parser.add_argument('-d','-dest',"--destinationId", type=int, nargs=None, help="The Destination Id to update data for", required=True)
        parser.add_argument('-ci','-cid',"--countryId", type=int, nargs=None, help="The Country Id to update the destinatin field to")
        parser.add_argument('-cc','-code',"--countryCode", type=str, nargs=None, help=r"The Iso Code of the country to assign to the Destination eg 'en' for Englang")
        parser.add_argument('-n',"--name", type=str, nargs=None, help="The name of the Destination")
        parser.add_argument('-a','--setActive', action='store_true', help="Makes the Destination Active")
        parser.add_argument('-i','--setInactive', action='store_true', help="Makes the Destination Inactive")
        parser.add_argument('-udel','--undoDeletion', action='store_true', help="Undoes the deletion of the Destination")
        parser.set_defaults(command=self.run)
