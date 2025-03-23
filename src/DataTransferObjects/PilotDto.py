from dataclasses import dataclass
from datetime import datetime
from DataTransferObjects.Mappable import Mappable

@dataclass
class PilotDto(Mappable):
    Id : int 
    Name : str
    CreatedDate : datetime
    DeletedDate : datetime