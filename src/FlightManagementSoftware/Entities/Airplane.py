from dataclasses import dataclass
from datetime import datetime
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.EntityBase import EntityBase


@dataclass
class Airplane(EntityBase, Mappable):
    Id : int
    ModelNumber : str
    ManufacturedDate : datetime
    LastServiceDate : datetime
    PassengerCapacity : int
    CurrentDestinationId : int
    CreatedDate : datetime
    DeletedDate : datetime

    def Create(self):
        self._Create(self)


    def Update(self):
        self._Update(self)


    # When deleting an Airplane we also want to soft delete any of their pending flights
    def Delete(self):
        qry = r'''
            UPDATE Flight f SET f.DeletedDate = DATETIME('now') 
            
            WHERE f.AirplaneId = ?
                AND f.ArrivalTimeUTC IS NULL
                AND f.DepartureTimeUTC > DATETIME('now')
        '''
        with dbConnectionInstance.Get_Transaction() as transaction:
            transaction.execute(qry, self.Id)
            self._Delete(self, transaction)