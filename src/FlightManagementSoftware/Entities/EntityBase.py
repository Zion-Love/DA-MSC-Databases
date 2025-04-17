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
        qry = f'SELECT * FROM {cls.__name__};'

        return DataFrame(cls.Map(QueryResult(qry)), cls)
    

    @classmethod
    def QueryById(cls, Id : list[int] | int):

        if(not issubclass(cls,Mappable)):
            raise Exception("Entity Base must inherit Mappable")
        qry = f'SELECT * FROM {cls.__name__}'

        if isinstance(Id, list) and all([isinstance(i,int) for i in Id]):
            if len(Id) == 0:
                raise Exception(f"Ids are empty when calling {cls.__name__}.QueryById")
            qry += f" WHERE Id in ({','.join(['?'] * len(Id))})"
            result = cls.Map(QueryResult(qry,Id))
            return None if result == None else result
        elif isinstance(Id, int):
            qry += " WHERE Id = ?"
            result = cls.Map(QueryResult(qry,Id).AssertSingle())
            return None if result == None else result[0]
        else:
            raise Exception(f"Could not search for Ids {Id} in {cls.__name__}.QueryById")
        

    @classmethod
    def _DeleteById(cls, Id : int | list[int]):
        parameters = []
        softDeleteColumn = [f.name for f in fields(cls) if f.name in ['DeletionDate', 'DeletedDate']]

        if len(softDeleteColumn) == 1:
            qry = f'UPDATE {cls.__name__} SET {softDeleteColumn} = {datetime.now()} WHERE Id'
        else:
            qry = f'DELETE FROM {cls.__name__} WHERE Id'

        if isinstance(Id, int):
            qry += " = ?"
            parameters.append(Id)
        elif isinstance(Id, list) and len(Id) > 0:
            qry += f" in ({['?' * len(Id)]})"
            parameters.extend(Id)
        else:
            raise Exception("No ides provided to delete")
        
        QueryResult(qry, *parameters)
    

    # Each of these operations accept a transaction variable , this means
    # we can bespoke handle dependant operations in the subclass implementation
    # of the corresponding abstract methods Create, Delete, Update ...

    # I should convert to using instance fields rather than looking for presence of Id column
    # this is only relevant for PilotFlight that has no Id column
    # Since it is the only entity not using this I will just overwrite this behaviour inside its Delete implementation
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


    # Generic update method from in memeory representation of entity record
    @classmethod
    def _Update(cls, instance, transaction = None):
        columns = [f.name for f in fields(cls) if f.name != 'Id']
        qry = f'''
            UPDATE {cls.__name__} SET {str.join(', ',[ f'{c} = ?' for c in columns])} WHERE Id = ?
        '''
        print(qry)

        params = [instance.__dict__[column] for column in columns] 
        params.append(instance.Id)
        if(transaction != None):
            transaction.execute(qry, *params)
        else :
            with(dbConnectionInstance.Get_Transaction() as transaction):
                transaction.execute(qry, params)


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
    