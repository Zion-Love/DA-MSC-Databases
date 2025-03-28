from dataclasses import dataclass
from Entities import Pilot

@dataclass
class EntityMap:
    Pilot : Pilot

entityMap = EntityMap(Pilot=Pilot)