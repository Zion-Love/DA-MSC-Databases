from FlightManagementSoftware.db.sqlite import dbConnectionInstance

class QueryResult:
    def __init__(self, query : str, *parameters):
        # store query next to result for debugging
        self.query = query
        self.parameters = tuple(parameters)
        # perform query agaisnt db
        with(dbConnectionInstance.Get_Transaction() as transaction):
            if not parameters:
                self.cursor = transaction.execute(query)
            else :
                self.cursor = transaction.execute(query, self.parameters)
            self.result = self.cursor.fetchall()


    def AssertSingleOrNull(self):
        if(not len(self.result) <= 1):
            raise Exception(f"Query : {self.query} Expected 1 or no results, instead got : {len(self.result)} \n {self.result}")
        return self


    def AssertSingle(self):
        if(not len(self.result) == 1):
            raise Exception(f"Query : {self.query} Expected exactly 1 result, instead got : {len(self.result)} \n {self.result}")
        return self
            
        
