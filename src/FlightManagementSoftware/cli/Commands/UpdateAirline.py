# TODO

from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler
from FlightManagementSoftware.cli.CommandParser import CommandParser
from FlightManagementSoftware.Entities.Airline import Airline

'''
    This Commadn will Update an Airline record using the supplied data

'''
@dataclass
class UpdateAirlineCommand(CommandHandler):
    
    def Validate(self):
        pass

    def Handle(self):
        pass