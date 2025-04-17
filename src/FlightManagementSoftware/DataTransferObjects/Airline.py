from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

'''
a.Id as AirlineId, a.Name, ActivePilots.cnt as ActivePilots, InactivePilots.cnt as InactivePilots,
        a.CreatedDate, a.DeletedDate

'''
@dataclass
class AirlinePilotSummary(Mappable):
    AirlineId : int
    Name : str
    ActivePilots : int
    InactivePilots : int
    CreatedDate : datetime
    DeletedDate : datetime