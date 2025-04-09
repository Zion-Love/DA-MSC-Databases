from dataclasses import dataclass
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.Entities.EntityBase import EntityBase
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable


class PilotFlight(EntityBase, Mappable):
    PilotId : int
    FlightId : int

    # PK constraint will handle preventing duplicate assignment
    def Create(self):
        PilotFlight._Create(self)

    # Pilot flight assignment should only be either this record exists = assigned to flight or no record = not assigned
    def Update(self):
        pass

    def Delete(self):
        PilotFlight.Delete()