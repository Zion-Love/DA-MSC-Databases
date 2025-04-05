from dataclasses import dataclass
from datetime import datetime
from DataFrame import DataFrame
from cli.CommandHandler import CommandHandler
from repositories.PilotRepository import pilotRepository

'''
    Request to view a secific pilots flight schedule, requires the pilotId
'''

@dataclass
class ViewPilotFlightScheduleCommand(CommandHandler):
    pilotId : int
    startDate : datetime
    endDate : datetime
    includeDeletedFlights : bool = False


    def Validate(self):
        assert(self.startDate < self.endDate)
        assert(isinstance(self.pilotId, int) and self.pilotId != None)


    def Handle(self):
        flightScheduleInformation : DataFrame = (
            pilotRepository
            .QueryPilotFlightSchedule(
                self.pilotId,
                self.includeDeletedFlights,
                self.startDate,
                self.endDate
            )
        )
        print(flightScheduleInformation)

        