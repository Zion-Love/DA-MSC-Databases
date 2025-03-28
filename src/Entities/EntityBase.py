from abc import ABC, abstractmethod
from datetime import datetime
from db.sqlite import dbConnectionInstance
from DataTransferObjects.Mappable import Mappable
from Entities.QueryResult import QueryResult
from DataFrame import DataFrame
from dataclasses import fields

class EntityBase(ABC):
    '''
        For EntityBase objects all subclases MUST overide CRUD operations, this is to ensure our python object representation is that of a specific table

        It is similar to a repository although more complex querying logic IE across multiple tables will be performed by repositories

        Basic functions like QueryAll and QueryById are here too since all tables have this functionality
    '''
    @classmethod
    def QueryAll(cls) -> DataFrame:
        if(not issubclass(cls,Mappable)):
            raise Exception("Entity Base must inherit Mappable")
        qry = f'SELECT * FROM {cls.__name__};'

        return DataFrame(cls.Map(QueryResult(qry)))
    

    @classmethod
    def QueryById(cls, Id : int):
        if(not issubclass(cls,Mappable)):
            raise Exception("Entity Base must inherit Mappable")
        qry = f'SELECT * FROM {cls.__name__} WHERE Id = ?'

        return DataFrame(cls.Map(QueryResult(qry,Id)))
    
    
    # deleted database record that matches in memory record Id
    @classmethod
    def _Delete(cls, instance):
        # infering soft delete from presence of column DeletedDate
        with(dbConnectionInstance.Get_Transaction() as transaction):
            if len([f.name for f in fields(cls) if f.name == "DeletedDate"]) == 0:
                qry = f'DELETE FROM  {cls.__name__} WHERE Id = ?'
                transaction.execute(qry, (instance.Id))
            else:
                qry = f'UPDATE {cls.__name__} SET DeletedDate = ? WHERE Id = ?'
                transaction.execute(qry, (datetime.now(), instance.Id))


    @classmethod
    def _Create(cls, instance):
        if(instance.Id != None):
            raise Exception(f"Entity record for {cls.__name__} already exists with id : {instance.Id} consider calling Update instead")
        
        columns = [f.name for f in fields(cls) if f.name != 'Id']
        qry = f'''
            INSERT INTO {cls.__name__} ({str.join(', ',columns)}) VALUES ({str.join(', ', ['?'] * len(columns))})
        '''
        with(dbConnectionInstance.Get_Transaction() as transaction):
            transaction.execute(qry, tuple([instance[column] for column in columns]))
            instance.Id = transaction.lastrowid


    # Uses our in memory instance to update mathing Id record columns to our in memory instance values
    @classmethod
    def _Update(cls, instance):
        columns = [f.name for f in fields(cls) if f.name != 'Id']
        qry = f'''
            UPDATE {cls.__name__} ({str.join(', ',columns)}) VALUES ({str.join(', ', ['?'] * len(columns))}) WHERE Id = ?
        '''
        with(dbConnectionInstance.Get_Transaction() as transaction):
            transaction.execute(qry, tuple([instance[column] for column in columns].append(instance.Id)))


    @abstractmethod
    def Create(self, *args, **kwargs):
        raise NotImplementedError()
    

    @abstractmethod
    def Update(self, *args, **kwargs):
        raise NotImplementedError()
    

    @abstractmethod
    def Delete(self, *args, **kwargs):
        raise NotImplementedError()
    