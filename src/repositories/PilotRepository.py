from repositories.RepositoryBase import RepositoryBase
from Entities.QueryResult import QueryResult

'''
    Working with a psuedo repository like pattern to define all my queries targetting specific tables in one place

    I say Psuedo because ideally this would be using dependancy injection to prevent the need to explicitly pass the instance
    into code requiring it but I dont have time to figure out how to do that with build-in pytho libs

    a massive improvement to all of this would be to not use raw sql here , instead to use an object instance that defines the target table
    along with the ability to apply filters / ordering conditions using ORM like syntax
'''
class PilotRepository(RepositoryBase):
    def __init__(self):
        super().__init__()
        pass

    # TODO : Create generic validation for sql paramaters to try to circumvent SQL injection
    def QueryById(self, pilotId : int) -> QueryResult:
        query = f'''
            SELECT * from Pilot p WHERE p.Id = {str(pilotId)};
        '''
        return QueryResult(query=query).AssertSingleOrNull()

    def QueryByName(self, name : str) -> QueryResult:
        query = f'''
            SELECT * from Pilot p WHERE p.\"Name\" = {name};
        '''
        return QueryResult(query=query).AssertSingleOrNull()
    
    def QueryAll(self, filterDeleted : bool = True):
        query = f'''
            SELECT * from Pilot p 
        '''
        if filterDeleted: query += ' WHERE p.DeletedDate is NULL'
        query += ';'
        return QueryResult(query=query)
    
pilotRepository : PilotRepository = PilotRepository()