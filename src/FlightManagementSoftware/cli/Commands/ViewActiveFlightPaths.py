from dataclasses import dataclass
from FlightManagementSoftware.cli.CommandHandler import CommandHandler

'''
    This command will read and show all the flight paths

    can be filtered by:
        Inactive : if false includes all deleted flights 
        CountryCodes : only include flights to / from selected countries , found by their codes
        StartDate : Only include flights whose CreatedDate >= StartDate
        EndDate : Only include flights whose CreatedDate <= EndDate
'''

@dataclass
class ViewFlightPathsCommand(CommandHandler):
    FilterCountryCodes: list[str] = None
    ShowInactivePaths: bool = False
    
    def Validate(self):
        raise NotImplementedError()
    
    def Handle(self):
        raise NotImplementedError()
