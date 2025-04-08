from dataclasses import dataclass
from Entities import (
    Pilot,
    Destination,
    Flight
)
# THIS MAY NOT BE NEEDED ...

@dataclass
class EntityMap:
    Pilot: Pilot
    Destination: Destination
    Flight: Flight

entityMap = EntityMap(
    Pilot=Pilot,
    Destination=Destination,
    Flight=Flight
)
