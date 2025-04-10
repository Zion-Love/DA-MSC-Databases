from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import fields
from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable
from FlightManagementSoftware.Entities.QueryResult import QueryResult
from FlightManagementSoftware.DataTransferObjects.DataFrame import DataFrame

dbColumnTypeMap = {
    int : 'INTEGER',
    str : 'TEXT',
    datetime : 'DATETIME2'
}

'''
    An Abstract Base Class (ABC) Used to template 'Entities' or objects that represent database tables directly

    It contains simple methods to Create , Update and Delete records by reflecting the calling subclass fields / name
'''

class EntityBase(ABC):
    @classmethod
    def QueryAll(cls) -> DataFrame:
        if(not issubclass(cls, Mappable)):
            raise Exception("Entity Base must inherit Mappable")
        qry = f'SELECT * FROM {cls.__name__};'

        return DataFrame(cls.Map(QueryResult(qry)))
    

    # not returning as dataframe since a single record is all thats needed
    # this way we can check the fields directly
    @classmethod
    def QueryById(cls, Id : int):
        if(not issubclass(cls,Mappable)):
            raise Exception("Entity Base must inherit Mappable")
        qry = f'SELECT * FROM {cls.__name__} WHERE Id = ?'

        result = cls.Map(QueryResult(qry,Id).AssertSingle())
        return None if result == None else result[0]
    

    # Each of these operations accept a transaction variable , this means
    # we can bespoke handle dependant operations in the subclass implementation
    # of the corresponding abstract methods Create, Delete, Update ...

    # TODO : investigate creating a decorator function to add this instead of drilling transaction through like this...
    # I should convert to using instance fields rather than looking for presence of Id column
    # this is only relevant for PilotFlight that has no Id column
    # Since it is the onl entity not using this I will just overwrite this behaviour inside its Delete implementation
    # for a larger scale project with multiple many to many relationship tables I would change this to be more generic
    # and not require the presence of an Id column
    
    # deleted database record that matches in memory record Id
    @classmethod
    def _Delete(cls, instance, transaction = None):
        # infering soft delete from presence of column DeletedDate
        qry = ''
        softdelete = len([f.name for f in fields(cls) if f.name == "DeletedDate"]) == 1
        if not softdelete:
            qry = f'DELETE FROM  {cls.__name__} WHERE Id = ?'
        else:
            qry = f'UPDATE {cls.__name__} SET DeletedDate = ? WHERE Id = ?'

        if transaction:
            if softdelete:
                transaction.execute(qry, (datetime.now(), instance.Id))
            else:
                transaction.execute(qry, (instance.Id,))
            return 

        with(dbConnectionInstance.Get_Transaction() as transaction):
                if softdelete:
                    transaction.execute(qry, (datetime.now(), instance.Id))
                else:
                    transaction.execute(qry, (instance.Id,))


    @classmethod
    def _Create(cls, instance, transaction = None):
        # The Id column is populated by the database using the Identity Autoincrement column constraints, and then fetched using lastrowid
        if(instance.Id != None):
            raise Exception(f"Entity record for {cls.__name__} already exists with id : {instance.Id} consider calling Update instead")
        
        columns = [f.name for f in fields(cls) if f.name != 'Id']
        qry = f'''
            INSERT INTO {cls.__name__} ({str.join(', ',columns)}) VALUES ({str.join(', ', ['?'] * len(columns))})
        '''
        if(transaction != None):
            transaction.execute(qry, tuple([getattr(instance,column) for column in columns]))
        else :
            with(dbConnectionInstance.Get_Transaction() as transaction):
                transaction.execute(qry, tuple([getattr(instance,column) for column in columns]))

        instance.Id = transaction.lastrowid


    # Uses our in memory instance to update mathing Id record columns to our in memory instance values
    @classmethod
    def _Update(cls, instance, transaction = None):
        columns = [f.name for f in fields(cls) if f.name != 'Id']
        qry = f'''
            UPDATE {cls.__name__} ({str.join(', ',columns)}) VALUES ({str.join(', ', ['?'] * len(columns))}) WHERE Id = ?
        '''
        print(qry)
        if(transaction != None):
            transaction.execute(qry, tuple([instance.__dict__[column] for column in columns]))
        else :
            with(dbConnectionInstance.Get_Transaction() as transaction):
                transaction.execute(qry, tuple([instance.__dict__[column] for column in columns].append(instance.Id)))


    # these methods are required overrides for a subclass of EntityBase to be valid

    @abstractmethod
    def Create(self):
        raise NotImplementedError()
    

    @abstractmethod
    def Update(self):
        raise NotImplementedError()
    

    @abstractmethod
    def Delete(self):
        raise NotImplementedError()
    